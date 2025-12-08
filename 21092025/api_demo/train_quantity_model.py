"""
Train Beer Sales Quantity Prediction Model (Quartiles)
Predicts beer selling quantity in 4 quartiles (Q1, Q2, Q3, Q4)
Based on beer_sales_prediction.ipynb
"""
import pandas as pd
import numpy as np
import joblib
import h3
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import shared utilities
import sys
sys.path.insert(0, str(Path(__file__).parent))
from utils import simple_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Make tokenizer available for pickle compatibility
import __main__
__main__.simple_tokenizer = simple_tokenizer


def load_data(data_dir: str = "../") -> pd.DataFrame:
    """Load and merge all required data files"""
    print("=" * 70)
    print("Loading Data...")
    print("=" * 70)
    
    data_path = Path(data_dir)
    
    # Load main POI data
    print("📊 Loading HCMC_Raw_poi_withid.csv...")
    fuse_df = pd.read_csv(data_path / "HCMC_Raw_poi_withid.csv", low_memory=False)
    print(f"   ✓ Loaded {len(fuse_df):,} POIs")
    
    # Load labeled outlets
    print("📊 Loading Label_sellingbeerOutlet.xlsx...")
    outlet_df = pd.read_excel(data_path / "Label_sellingbeerOutlet.xlsx")
    print(f"   ✓ Loaded {len(outlet_df):,} labeled outlets")
    
    # Load volume data
    print("📊 Loading vol_HCMC.csv...")
    vol_df = pd.read_csv(data_path / "vol_HCMC.csv")
    print(f"   ✓ Loaded {len(vol_df):,} volume records")
    
    # Merge labeled outlets
    print("\n🔄 Merging data...")
    merged_df = fuse_df.merge(
        outlet_df[['ShopCode', 'beer_selling_outlet_potential_level']],
        how='left',
        left_on='poi_id',
        right_on='ShopCode'
    ).drop('ShopCode', axis=1)
    print(f"   ✓ Merged outlets: {len(merged_df):,} records")
    
    # Merge volume data
    merged_df = merged_df.merge(
        vol_df[['ShopCode', 'Vol']],
        how='left',
        left_on='poi_id',
        right_on='ShopCode'
    ).drop('ShopCode', axis=1)
    print(f"   ✓ Merged volumes: {len(merged_df):,} records")
    
    # Ensure hexagon column exists
    if 'idx_r9_hex' not in merged_df.columns or merged_df['idx_r9_hex'].isna().all():
        print("\n🔷 Calculating H3 hexagons from coordinates...")
        valid_mask = merged_df[['latitude', 'longitude']].notna().all(axis=1)
        if valid_mask.sum() > 0:
            lats = merged_df.loc[valid_mask, 'latitude'].values
            lons = merged_df.loc[valid_mask, 'longitude'].values
            hexagons = [h3.latlng_to_cell(lat, lon, 9) for lat, lon in zip(lats, lons)]
            merged_df.loc[valid_mask, 'idx_r9_hex'] = hexagons
            print(f"   ✓ Calculated {valid_mask.sum():,} hexagons")
    
    return merged_df


def create_quartiles(df: pd.DataFrame) -> pd.DataFrame:
    """Create quartile bins from Vol column"""
    print("\n" + "=" * 70)
    print("Creating Quartile Bins...")
    print("=" * 70)
    
    # Filter to outlets with Vol >= 1
    df_vol = df[df["Vol"].notnull() & (df["Vol"] >= 1)].copy()
    print(f"📊 Outlets with Vol >= 1: {len(df_vol):,}")
    
    if len(df_vol) == 0:
        raise ValueError("No outlets with Vol >= 1 found!")
    
    # Create quartiles using pd.qcut
    print("\n📊 Creating quartiles (Q1, Q2, Q3, Q4)...")
    df_vol["vol_bin"], bins = pd.qcut(
        df_vol["Vol"],
        q=[0, 0.25, 0.5, 0.75, 1.0],
        labels=[1, 2, 3, 4],  # Q1=1, Q2=2, Q3=3, Q4=4
        retbins=True
    )
    
    print(f"   ✓ Bin edges: {bins}")
    print(f"\n📊 Quartile distribution:")
    quartile_counts = df_vol["vol_bin"].value_counts().sort_index()
    for q, count in quartile_counts.items():
        print(f"   Q{q}: {count:,} outlets ({count/len(df_vol)*100:.1f}%)")
    
    return df_vol, bins


def prepare_features(df: pd.DataFrame) -> tuple:
    """Prepare features for training"""
    print("\n" + "=" * 70)
    print("Preparing Features...")
    print("=" * 70)
    
    # Define features (same as binary classification model)
    numeric_features = [
        "avg_rating", "reviews_number", "last_avg_rating",
        "last_1_reviews_number", "last_2_reviews_number",
        'latitude', 'longitude'
    ]
    
    categorical_features = [
        "location_type_resolved", "province_name", "ward_name",
        "idx_r9_hex"
    ]
    
    text_feature = "name"
    
    print(f"📊 Numeric features: {len(numeric_features)}")
    print(f"   {numeric_features}")
    print(f"\n📊 Categorical features: {len(categorical_features)}")
    print(f"   {categorical_features}")
    print(f"\n📊 Text feature: {text_feature}")
    
    # Extract features
    X_numeric = df[numeric_features].copy()
    X_categorical = df[categorical_features].copy()
    X_text = df[text_feature].fillna("").astype(str)
    
    # Target variable
    y = df["vol_bin"].copy()
    
    print(f"\n✓ Prepared features for {len(df):,} samples")
    print(f"✓ Target distribution: {y.value_counts().sort_index().to_dict()}")
    
    return X_numeric, X_categorical, X_text, y, numeric_features, categorical_features


def create_preprocessor(numeric_features, categorical_features):
    """Create preprocessing pipeline"""
    print("\n🔧 Creating preprocessing pipeline...")
    
    # Numeric preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical preprocessing
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # Combine preprocessors
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='drop'
    )
    
    print("   ✓ Preprocessor created")
    return preprocessor


def train_model(X_numeric, X_categorical, X_text, y, preprocessor, 
                numeric_features, categorical_features, random_state=42):
    """Train LightGBM model for quartile prediction"""
    print("\n" + "=" * 70)
    print("Training Model...")
    print("=" * 70)
    
    # Prepare text features (TF-IDF)
    print("📝 Processing text features (TF-IDF)...")
    tfidf = TfidfVectorizer(
        tokenizer=simple_tokenizer,
        max_features=9000,
        ngram_range=(1, 2),
        min_df=2
    )
    X_text_tfidf = tfidf.fit_transform(X_text)
    print(f"   ✓ TF-IDF features: {X_text_tfidf.shape[1]:,} dimensions")
    
    # Combine all features
    print("\n🔄 Combining features...")
    X_processed = preprocessor.fit_transform(
        pd.concat([X_numeric, X_categorical], axis=1)
    )
    print(f"   ✓ Processed features: {X_processed.shape[1]:,} dimensions")
    
    # Combine numeric/categorical with text
    from scipy.sparse import hstack
    X_combined = hstack([X_processed, X_text_tfidf])
    print(f"   ✓ Combined features: {X_combined.shape[1]:,} total dimensions")
    
    # Split data
    print("\n📊 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_combined, y,
        test_size=0.2,
        random_state=random_state,
        stratify=y  # Stratify by quartile
    )
    print(f"   ✓ Training set: {X_train.shape[0]:,} samples")
    print(f"   ✓ Test set: {X_test.shape[0]:,} samples")
    
    # Train model
    print("\n🤖 Training LightGBM Classifier...")
    model = lgb.LGBMClassifier(
        n_estimators=500,
        learning_rate=0.05,
        class_weight='balanced',  # Handle class imbalance
        random_state=random_state,
        verbose=-1
    )
    
    model.fit(X_train, y_train)
    print("   ✓ Model trained")
    
    # Evaluate
    print("\n📊 Evaluating model...")
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    
    print(f"   ✓ Training accuracy: {train_acc:.4f} ({train_acc*100:.2f}%)")
    print(f"   ✓ Test accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    
    # Classification report
    print("\n📋 Classification Report (Test Set):")
    print(classification_report(y_test, y_test_pred, 
                                target_names=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)']))
    
    # Confusion matrix
    print("\n📊 Confusion Matrix (Test Set):")
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'],
                yticklabels=['Q1 (Lowest)', 'Q2', 'Q3', 'Q4 (Highest)'])
    plt.title('Confusion Matrix (Quartile Bins)')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    confusion_matrix_path = Path(__file__).parent.parent / "model" / "quantity_confusion_matrix.png"
    confusion_matrix_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(confusion_matrix_path, dpi=150, bbox_inches='tight')
    print(f"\n   ✓ Saved confusion matrix to {confusion_matrix_path}")
    
    return model, tfidf, preprocessor, {
        'train_accuracy': float(train_acc),
        'test_accuracy': float(test_acc),
        'n_features': int(X_combined.shape[1]),
        'n_train_samples': int(X_train.shape[0]),
        'n_test_samples': int(X_test.shape[0]),
        'quartile_distribution': y.value_counts().sort_index().to_dict()
    }


def save_model(model, tfidf, preprocessor, metadata, bins, model_dir="../model"):
    """Save trained model and metadata"""
    print("\n" + "=" * 70)
    print("Saving Model...")
    print("=" * 70)
    
    model_path = Path(model_dir)
    model_path.mkdir(parents=True, exist_ok=True)
    
    # Save model with prefix "quantity"
    model_file = model_path / "quantity_lightgbm_classifier.pkl"
    joblib.dump(model, model_file)
    print(f"✓ Saved model to {model_file}")
    
    # Save TF-IDF vectorizer
    tfidf_file = model_path / "quantity_tfidf_vectorizer.pkl"
    joblib.dump(tfidf, tfidf_file)
    print(f"✓ Saved TF-IDF vectorizer to {tfidf_file}")
    
    # Save preprocessor
    preprocessor_file = model_path / "quantity_preprocessor.pkl"
    joblib.dump(preprocessor, preprocessor_file)
    print(f"✓ Saved preprocessor to {preprocessor_file}")
    
    # Save metadata including bin edges
    metadata['bin_edges'] = bins.tolist()
    metadata_file = model_path / "quantity_model_metadata.pkl"
    joblib.dump(metadata, metadata_file)
    print(f"✓ Saved metadata to {metadata_file}")
    
    print("\n" + "=" * 70)
    print("✅ Model Training Complete!")
    print("=" * 70)
    print(f"\n📁 Saved files:")
    print(f"   - {model_file.name}")
    print(f"   - {tfidf_file.name}")
    print(f"   - {preprocessor_file.name}")
    print(f"   - {metadata_file.name}")
    print(f"\n📊 Model Performance:")
    print(f"   - Test Accuracy: {metadata['test_accuracy']*100:.2f}%")
    print(f"   - Features: {metadata['n_features']:,}")
    print(f"   - Training Samples: {metadata['n_train_samples']:,}")
    print(f"   - Test Samples: {metadata['n_test_samples']:,}")


def main():
    """Main training pipeline"""
    print("\n" + "=" * 70)
    print("Beer Sales Quantity Prediction Model Training")
    print("Predicting Quartiles (Q1, Q2, Q3, Q4)")
    print("=" * 70)
    
    # Step 1: Load data
    df = load_data()
    
    # Step 2: Create quartiles
    df_vol, bins = create_quartiles(df)
    
    # Step 3: Prepare features
    X_numeric, X_categorical, X_text, y, numeric_features, categorical_features = prepare_features(df_vol)
    
    # Step 4: Create preprocessor
    preprocessor = create_preprocessor(numeric_features, categorical_features)
    
    # Step 5: Train model
    model, tfidf, preprocessor, metadata = train_model(
        X_numeric, X_categorical, X_text, y, preprocessor,
        numeric_features, categorical_features
    )
    
    # Step 6: Save model
    save_model(model, tfidf, preprocessor, metadata, bins)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()






