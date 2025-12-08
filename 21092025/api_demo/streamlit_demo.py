"""
Streamlit Demo for Beer Sales Prediction API
Interactive web interface for predicting beer-selling potential
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Optional
import time
import os
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Heineken - Beer Sales Potential Predictor",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Heineken branding
st.markdown("""
    <style>
    /* Heineken Brand Colors */
    :root {
        --heineken-green: #00A651;
        --heineken-red: #D71E24;
        --heineken-dark: #1A1A1A;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #00A651;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .high-potential {
        background: linear-gradient(135deg, #00A651 0%, #008040 100%);
        color: white;
    }
    .medium-potential {
        background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%);
        color: white;
    }
    .low-potential {
        background: linear-gradient(135deg, #D71E24 0%, #B01A1F 100%);
        color: white;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    /* Heineken sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar - Heineken Logo and Configuration
with st.sidebar:
    # Display Heineken Logo
    try:
        logo_path = Path(__file__).parent / "heineken_logo.svg"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            # Fallback: Display text logo
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="color: #00A651; font-size: 2rem; margin: 0;">HEINEKEN</h1>
                <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">Beer Sales Potential Predictor</p>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #00A651; font-size: 2rem; margin: 0;">HEINEKEN</h1>
            <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">Beer Sales Potential Predictor</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

# Configuration - Use Streamlit secrets (for Streamlit Cloud), environment variable, or default to localhost
try:
    # Try to get from Streamlit secrets first (for Streamlit Cloud deployment)
    DEFAULT_API_URL = st.secrets.get("API_URL", None)
    if DEFAULT_API_URL is None:
        DEFAULT_API_URL = os.getenv("API_URL", "http://localhost:8000")
except:
    # Fallback to environment variable or default
    DEFAULT_API_URL = os.getenv("API_URL", "http://localhost:8000")

API_URL = st.sidebar.text_input(
    "API URL", 
    value=DEFAULT_API_URL,
    help="URL of the running API server"
)

# Initialize session state
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []


def check_api_health(api_url: str):
    """Check if API is running and get health info"""
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except:
        return False, None


def predict_from_url(api_url: str, google_maps_url: str) -> Optional[Dict]:
    """Make prediction using auto-scrape endpoint"""
    try:
        response = requests.post(
            f"{api_url}/predict",
            json={"google_maps_url": google_maps_url},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def predict_manual(
    api_url: str, 
    google_maps_url: str,
    rating: Optional[float] = None,
    reviews: Optional[int] = None,
    category: Optional[str] = None,
    address: Optional[str] = None
) -> Optional[Dict]:
    """Make prediction with manual data input"""
    try:
        payload = {
            "google_maps_url": google_maps_url,
            "rating": rating,
            "reviews": reviews,
            "category": category,
            "address": address
        }
        response = requests.post(
            f"{api_url}/predict-manual",
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def get_confidence_color(confidence: float) -> str:
    """Get color based on confidence level"""
    if confidence >= 0.8:
        return "high-potential"
    elif confidence >= 0.6:
        return "medium-potential"
    elif confidence >= 0.4:
        return "medium-potential"
    else:
        return "low-potential"


def create_confidence_gauge(confidence: float):
    """Create a gauge chart for confidence"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Confidence Score (%)"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "gray"},
                {'range': [60, 80], 'color': "lightblue"},
                {'range': [80, 100], 'color': "blue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig


def create_features_chart(features: Dict):
    """Create a bar chart of key features"""
    feature_data = {
        'Feature': [],
        'Value': []
    }
    
    # Numeric features
    if features.get('avg_rating'):
        feature_data['Feature'].append('Average Rating')
        feature_data['Value'].append(features['avg_rating'])
    
    if features.get('reviews_number'):
        feature_data['Feature'].append('Number of Reviews')
        feature_data['Value'].append(min(features['reviews_number'] / 100, 10))  # Normalize for display
    
    if features.get('latitude'):
        feature_data['Feature'].append('Latitude')
        feature_data['Value'].append(features['latitude'])
    
    if features.get('longitude'):
        feature_data['Feature'].append('Longitude')
        feature_data['Value'].append(features['longitude'])
    
    if feature_data['Feature']:
        df = pd.DataFrame(feature_data)
        fig = px.bar(
            df, 
            x='Feature', 
            y='Value',
            title="Key Features",
            color='Value',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=300, showlegend=False)
        return fig
    return None


def create_feature_distribution_charts(features: Dict):
    """Create distribution charts for numeric features with reference ranges"""
    charts = []
    
    # Reference ranges based on typical values for HCMC beer-selling outlets
    reference_ranges = {
        'avg_rating': {
            'min': 3.5, 'max': 4.8, 'typical': 4.2, 
            'label': 'Average Rating (1-5)',
            'good_range': (4.0, 5.0),
            'description': 'Higher ratings indicate better customer satisfaction'
        },
        'reviews_number': {
            'min': 10, 'max': 5000, 'typical': 500,
            'label': 'Number of Reviews',
            'good_range': (100, 10000),
            'description': 'More reviews suggest established business'
        },
        'latitude': {
            'min': 10.3, 'max': 11.2, 'typical': 10.8,
            'label': 'Latitude (HCMC: ~10.8)',
            'good_range': (10.5, 11.0),
            'description': 'Location within Ho Chi Minh City'
        },
        'longitude': {
            'min': 106.3, 'max': 107.0, 'typical': 106.7,
            'label': 'Longitude (HCMC: ~106.7)',
            'good_range': (106.5, 107.0),
            'description': 'Location within Ho Chi Minh City'
        },
    }
    
    for feature_key, ref_range in reference_ranges.items():
        value = features.get(feature_key)
        if value is not None and value != 'N/A' and isinstance(value, (int, float)):
            try:
                value = float(value)
                # Create a horizontal bar chart showing value position
                fig = go.Figure()
                
                # Background range (typical range)
                fig.add_trace(go.Bar(
                    x=[ref_range['max'] - ref_range['min']],
                    y=[ref_range['label']],
                    base=[ref_range['min']],
                    orientation='h',
                    marker=dict(color='lightgray', opacity=0.3),
                    showlegend=False,
                    hoverinfo='skip',
                    name='Typical Range'
                ))
                
                # Good range highlight
                if 'good_range' in ref_range:
                    good_min, good_max = ref_range['good_range']
                    fig.add_trace(go.Bar(
                        x=[good_max - good_min],
                        y=[ref_range['label']],
                        base=[good_min],
                        orientation='h',
                        marker=dict(color='lightgreen', opacity=0.5),
                        showlegend=False,
                        hoverinfo='skip',
                        name='Good Range'
                    ))
                
                # Typical value line
                fig.add_trace(go.Scatter(
                    x=[ref_range['typical'], ref_range['typical']],
                    y=[ref_range['label'], ref_range['label']],
                    mode='lines',
                    line=dict(width=2, color='blue', dash='dash'),
                    showlegend=False,
                    name='Typical',
                    hovertemplate='Typical: %{x:.2f}<extra></extra>'
                ))
                
                # Current value marker
                in_range = ref_range['min'] <= value <= ref_range['max']
                in_good_range = 'good_range' in ref_range and ref_range['good_range'][0] <= value <= ref_range['good_range'][1]
                color = 'green' if in_good_range else ('orange' if in_range else 'red')
                
                fig.add_trace(go.Scatter(
                    x=[value],
                    y=[ref_range['label']],
                    mode='markers+text',
                    marker=dict(size=15, color=color, symbol='circle', line=dict(width=2, color='white')),
                    text=[f"{value:.2f}"],
                    textposition='middle right',
                    showlegend=False,
                    name='Current',
                    hovertemplate='Current: %{x:.2f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title=f"{ref_range['label']}<br><sub>{ref_range.get('description', '')}</sub>",
                    xaxis=dict(
                        range=[ref_range['min'] - (ref_range['max'] - ref_range['min']) * 0.2,
                               ref_range['max'] + (ref_range['max'] - ref_range['min']) * 0.2],
                        title='Value'
                    ),
                    yaxis=dict(showgrid=False, showticklabels=False),
                    height=120,
                    margin=dict(l=10, r=10, t=60, b=10),
                    hovermode='closest'
                )
                
                charts.append((feature_key, fig))
            except (ValueError, TypeError):
                continue
    
    return charts


def create_result_explanation(result: Dict, features: Dict):
    """Create detailed explanation of the prediction result"""
    confidence = result.get('confidence', 0)
    prediction_label = result.get('prediction_label', 'Unknown')
    
    explanations = []
    
    # Confidence-based explanation
    if confidence >= 0.8:
        explanations.append({
            'icon': '✅',
            'title': 'Very High Confidence',
            'text': f'The model is {result.get("confidence_percentage", "N/A")} confident this location is a beer seller. This is based on strong indicators in the features.'
        })
    elif confidence >= 0.6:
        explanations.append({
            'icon': '⚠️',
            'title': 'High Confidence',
            'text': f'The model is {result.get("confidence_percentage", "N/A")} confident. The location shows good potential but some factors may vary.'
        })
    elif confidence >= 0.4:
        explanations.append({
            'icon': '⚖️',
            'title': 'Moderate Confidence',
            'text': f'The model is {result.get("confidence_percentage", "N/A")} confident. This location has mixed indicators - consider additional market research.'
        })
    else:
        explanations.append({
            'icon': '❌',
            'title': 'Low Confidence',
            'text': f'The model is {result.get("confidence_percentage", "N/A")} confident this location is NOT a beer seller. The features suggest low potential.'
        })
    
    # Feature-based explanations
    rating = features.get('avg_rating')
    reviews = features.get('reviews_number', 0)
    category = features.get('location_type_resolved', 'Unknown')
    place_name = features.get('name', '')
    h3_index = features.get('idx_r9_hex')
    
    # Name/TF-IDF explanation (dynamic based on actual analysis)
    if place_name:
        tfidf_analysis = result.get('tfidf_analysis', {})
        important_terms = tfidf_analysis.get('important_terms', [])
        common_terms_found = tfidf_analysis.get('common_beer_terms_found', [])
        present_terms_count = len(tfidf_analysis.get('present_terms', []))
        
        # Build dynamic explanation
        explanation_text = f'''
        **Place Name**: "{place_name}"
        
        The model uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to analyze the place name. This converts the name into ~9,000 text features that capture:
        - **Keywords**: Words that indicate business type
        - **Semantic patterns**: The model learned which name patterns correlate with beer sales
        - **Language cues**: Vietnamese vs English names, formal vs casual naming
        
        **Analysis for this location:**
        - Found **{present_terms_count} TF-IDF features** in this name
        '''
        
        if important_terms:
            # Show top important terms found in this name
            top_terms_display = ', '.join([f'"{term}"' for term in important_terms[:5]])
            explanation_text += f'''
        - **Top important terms detected**: {top_terms_display}
        '''
        
        if common_terms_found:
            # Show which common beer-related terms were found
            common_display = ', '.join([f'"{term}"' for term in common_terms_found])
            explanation_text += f'''
        - **Beer-related keywords found**: {common_display}
        
        These keywords typically indicate higher beer sales potential, as they suggest restaurant/bar/cafe establishments where beer is commonly served.
        '''
        else:
            explanation_text += '''
        
        **Note**: No common beer-related keywords (like "Quán", "Restaurant", "Bar", "Pub") were detected in this name. The model still analyzes all text patterns, but the absence of these keywords may affect the prediction.
        '''
        
        explanations.append({
            'icon': '📝',
            'title': 'Place Name Analysis (TF-IDF)',
            'text': explanation_text
        })
    
    # Category explanation
    if category and category != 'Unknown' and category != 'N/A':
        category_lower = category.lower()
        category_impact = "high" if any(word in category_lower for word in ['restaurant', 'nhà hàng', 'quán', 'bar', 'pub', 'cafe']) else "moderate"
        
        explanations.append({
            'icon': '🏷️',
            'title': 'Location Category Impact',
            'text': f'''
            **Category**: {category}
            
            The location type is a **strong predictor** of beer sales potential:
            
            **High Potential Categories:**
            - 🍽️ Restaurants (Nhà hàng, Quán ăn)
            - 🍺 Bars & Pubs
            - ☕ Cafes with food service
            - 🍻 Beer gardens
            
            **Moderate Potential:**
            - Convenience stores
            - Supermarkets
            - Hotels with restaurants
            
            **Low Potential:**
            - Offices
            - Schools
            - Hospitals
            
            Your location's category ({category}) suggests **{category_impact} potential** for beer sales.
            '''
        })
    elif not category or category == 'Unknown' or category == 'N/A':
        explanations.append({
            'icon': '⚠️',
            'title': 'Category Not Available',
            'text': 'Category information could not be extracted. The model inferred a default category, which may affect prediction accuracy. Use Manual Input mode to provide the correct category for better results.'
        })
    
    # H3 Hexagon explanation
    if h3_index:
        explanations.append({
            'icon': '🔷',
            'title': 'H3 Geospatial Index (Hexagon)',
            'text': f'''
            **H3 Index**: `{h3_index}`
            
            The **H3 hexagon index** is a geospatial feature that divides the map into hexagonal cells. This helps the model understand:
            
            **What H3 Tells Us:**
            - 📍 **Location clustering**: Areas with many beer-selling outlets
            - 🗺️ **Geographic patterns**: Which neighborhoods/districts have high beer sales
            - 🏘️ **Area characteristics**: Urban vs suburban, commercial vs residential
            
            **Resolution 9** (idx_r9_hex) means each hexagon covers approximately:
            - ~0.46 km² (0.18 mi²)
            - About 2-3 city blocks in Ho Chi Minh City
            
            **How It Helps Prediction:**
            - The model learned which H3 hexagons have high concentrations of beer-selling outlets
            - Your location's hexagon `{h3_index}` is compared to training data
            - If similar hexagons had many beer sellers, your location scores higher
            
            This is especially useful for identifying **commercial districts** and **nightlife areas** where beer sales are common.
            '''
        })
    
    if rating and rating >= 4.0:
        explanations.append({
            'icon': '⭐',
            'title': 'High Rating',
            'text': f'Rating of {rating:.1f} indicates good customer satisfaction, which correlates with beer sales potential.'
        })
    
    if reviews and reviews >= 100:
        explanations.append({
            'icon': '👥',
            'title': 'Good Review Count',
            'text': f'{reviews:,} reviews suggest established business with customer base, favorable for beer sales.'
        })
    elif reviews == 0 or reviews is None:
        explanations.append({
            'icon': '⚠️',
            'title': 'Missing Review Data',
            'text': 'Review data could not be scraped. This may affect prediction accuracy. Consider using Manual Input mode.'
        })
    
    return explanations


def display_prediction_result(result: Dict):
    """Display prediction results with analytics"""
    if not result or not result.get('success'):
        st.error("Failed to get prediction result")
        return
    
    place_info = result.get('place_info', {})
    # Binary prediction confidence (Beer Sales Potential)
    beer_sales_confidence = result.get('confidence', 0)
    prediction_label = result.get('prediction_label', 'Unknown')
    risk_level = result.get('risk_level', 'Unknown')
    recommendation = result.get('recommendation', '')
    all_features = result.get('all_features', {})
    
    # Header with prediction
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### 📍 {place_info.get('name', 'Unknown Place')}")
        st.markdown(f"**Category:** {place_info.get('category', 'N/A')}")
        st.markdown(f"**Address:** {place_info.get('address', 'N/A')}")
    
    with col2:
        st.metric("Rating", f"{place_info.get('rating', 'N/A')} ⭐")
        st.metric("Reviews", f"{place_info.get('reviews', 0):,}")
    
    with col3:
        st.metric("Prediction", prediction_label)
        st.metric("Confidence", result.get('confidence_percentage', 'N/A'))
    
    # Quantity Prediction Section (if available and prediction is beer seller)
    quantity_pred = result.get('quantity_prediction')
    if quantity_pred and prediction_label == 'Beer Seller':
        st.markdown("---")
        st.markdown("## 📊 Beer Sales Quantity Prediction")
        
        quartile = quantity_pred.get('quartile', 0)
        quartile_label = quantity_pred.get('quartile_label', f'Q{quartile}')
        quantity_confidence = quantity_pred.get('confidence', 0)  # Renamed to avoid shadowing
        probabilities = quantity_pred.get('probabilities', {})
        interpretation = quantity_pred.get('interpretation', '')
        
        # Display quartile prediction
        col1, col2, col3, col4 = st.columns(4)
        
        quartile_colors = {1: '#e74c3c', 2: '#f39c12', 3: '#3498db', 4: '#2ecc71'}
        quartile_names = {1: 'Q1 (Lowest)', 2: 'Q2', 3: 'Q3', 4: 'Q4 (Highest)'}
        
        with col1:
            st.markdown(f"### {quartile_label}")
            st.markdown(f"**Predicted Quartile**")
            st.markdown(f"Confidence: **{quantity_confidence*100:.1f}%**")
        
        with col2:
            st.markdown("**Quartile Distribution:**")
            # Create a bar chart for quartile probabilities
            fig_quartile = go.Figure()
            for q in [1, 2, 3, 4]:
                prob = probabilities.get(f'Q{q}', 0)
                color = quartile_colors.get(q, '#95a5a6')
                fig_quartile.add_trace(go.Bar(
                    x=[quartile_names[q]],
                    y=[prob],
                    marker_color=color,
                    text=[f"{prob*100:.1f}%"],
                    textposition='auto',
                    name=quartile_names[q]
                ))
            fig_quartile.update_layout(
                height=200,
                showlegend=False,
                yaxis_title="Probability",
                yaxis=dict(range=[0, 1])
            )
            st.plotly_chart(fig_quartile, use_container_width=True)
        
        with col3:
            st.markdown("**Quartile Probabilities:**")
            for q in [1, 2, 3, 4]:
                prob = probabilities.get(f'Q{q}', 0)
                is_predicted = q == quartile
                marker = "✅" if is_predicted else "  "
                st.markdown(f"{marker} {quartile_names[q]}: {prob*100:.1f}%")
        
        with col4:
            st.markdown("**Interpretation:**")
            st.info(interpretation)
        
        # Explanation of quartiles
        with st.expander("ℹ️ Understanding Quartile Predictions", expanded=False):
            st.markdown("""
            **What are Quartiles?**
            
            The model predicts beer selling **quantity** by dividing outlets into 4 quartiles based on their sales volume:
            
            - **Q1 (Lowest)**: Bottom 25% of outlets by volume
            - **Q2**: 25-50% range
            - **Q3**: 50-75% range  
            - **Q4 (Highest)**: Top 25% of outlets by volume
            
            **How to Use This:**
            - **Q4 prediction** = High volume expected, prioritize this location
            - **Q3 prediction** = Good volume, solid opportunity
            - **Q2 prediction** = Moderate volume, consider other factors
            - **Q1 prediction** = Lower volume, may need marketing support
            
            **Note:** This prediction is only shown for locations predicted as "Beer Seller". 
            The quartile indicates the expected sales volume tier based on similar outlets in the training data.
            """)
        
        st.markdown("---")
    
    # Prediction box
    confidence_class = get_confidence_color(beer_sales_confidence)
    st.markdown(f"""
        <div class="prediction-box {confidence_class}">
            <h2 style="margin:0;">🎯 {prediction_label}</h2>
            <p style="font-size:1.2rem; margin:0.5rem 0;"><strong>Confidence: {result.get('confidence_percentage', 'N/A')}</strong></p>
            <p style="font-size:1rem; margin:0.5rem 0;"><strong>Risk Level: {risk_level}</strong></p>
            <p style="margin-top:1rem;">{recommendation}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sales Assignment Section (moved right after prediction)
    sales_assignment = result.get('sales_assignment')
    if sales_assignment:
        st.markdown("---")
        st.markdown("## 👥 Sales Assignment")
        
        channel = sales_assignment.get('channel')
        territory = sales_assignment.get('territory')
        sales_rep = sales_assignment.get('sales_rep')
        hex_id = sales_assignment.get('hex_id')
        used_parent_hexagon = sales_assignment.get('used_parent_hexagon', False)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Sales Channel")
            if channel:
                # Channel descriptions
                channel_descriptions = {
                    'MONT': 'Modern On-Trade (Restaurants, Bars, Hotels)',
                    'TONT': 'Traditional On-Trade (Quan Nhau, Quan An)',
                    'TOFT': 'Traditional Off-Trade (Wholesalers, Distributors)',
                    'MOFT': 'Modern Off-Trade (Supermarkets, Hypermarkets)',
                    'Other': 'Other Channels'
                }
                channel_desc = channel_descriptions.get(channel, channel)
                st.success(f"**{channel}**")
                st.caption(channel_desc)
            else:
                st.warning("Channel not assigned")
                st.caption("Category may not be mapped to a sales channel")
        
        with col2:
            st.markdown("### 🗺️ Assigned Territory")
            if territory:
                st.info(f"**{territory}**")
                if hex_id:
                    st.caption(f"HexID: `{hex_id}`")
                    if used_parent_hexagon:
                        st.caption("ℹ️ Using parent hexagon (resolution 8) - sales data uses resolution 8")
            else:
                st.warning("Territory not found")
                if channel and hex_id:
                    st.caption(f"HexID: `{hex_id}`")
                    st.caption(f"Location may not be assigned to {channel} channel territory")
                    st.caption("This hexagon may not have territory assignment for this channel")
                elif channel:
                    st.caption(f"Location may not be assigned to {channel} channel territory")
                else:
                    st.caption("Channel must be assigned first")
        
        with col3:
            st.markdown("### 👤 Sales Representative")
            if sales_rep:
                sr_name = sales_rep.get('srname', 'N/A')
                sr_id = sales_rep.get('srid', 'N/A')
                sr_email = sales_rep.get('srheiwayid', 'N/A')
                
                st.success(f"**{sr_name}**")
                if sr_id != 'N/A':
                    st.caption(f"ID: {sr_id}")
                if sr_email and sr_email != 'N/A':
                    st.caption(f"Email: {sr_email}")
            else:
                st.warning("Sales rep not assigned")
                if territory:
                    st.caption("Territory may not have assigned sales rep")
                else:
                    st.caption("Territory must be assigned first")
        
        # Sales Assignment Flow Diagram
        with st.expander("ℹ️ How Sales Assignment Works", expanded=False):
            st.markdown("""
            **Sales Assignment Flow:**
            
            1. **Category → Channel**: Place category (e.g., "Restaurant", "Bar") is mapped to a sales channel
               - Restaurant, Bar, Karaoke → `MONT` (Modern On-Trade)
               - Quan Nhau, Quan An → `TONT` (Traditional On-Trade)
               - Wholesaler, Distributor → `TOFT` (Traditional Off-Trade)
               - Supermarket, Hypermarket → `MOFT` (Modern Off-Trade)
            
            2. **Location → Territory**: Place location (lat/lon) is converted to H3 hexagon ID, 
               which is mapped to a territory for the assigned channel
            
            3. **Territory → Sales Rep**: Territory is mapped to the assigned sales representative
            
            **Note**: One location can serve multiple channels (e.g., a hexagon can have MONT, TONT, and TOFT channels),
            but the assignment shown is based on the place's category.
            """)
    
    # Scraping Warning and Fallback Info
    rating = place_info.get('rating')
    reviews = place_info.get('reviews', 0)
    
    # Check if rating might be from aggregated features (fallback)
    aggregated = result.get('aggregated_features', {})
    category_features = aggregated.get('category_features') or {}
    hexagon_features = aggregated.get('hexagon_features') or {}
    
    # If rating exists but seems to match aggregated averages, it's likely a fallback
    is_fallback_rating = False
    cat_rating = category_features.get('avg_rating') if category_features else None
    hex_rating = hexagon_features.get('avg_rating') if hexagon_features else None
    
    if rating and (cat_rating or hex_rating):
        if cat_rating and abs(rating - cat_rating) < 0.1:
            is_fallback_rating = True
        elif hex_rating and abs(rating - hex_rating) < 0.1:
            is_fallback_rating = True
        elif cat_rating and hex_rating:
            avg_rating = (cat_rating + hex_rating) / 2
            if abs(rating - avg_rating) < 0.1:
                is_fallback_rating = True
    
    if not rating or rating is None or reviews == 0:
        if is_fallback_rating or (category_features or hexagon_features):
            st.info("""
            ℹ️ **Using Estimated Rating from Aggregated Features**: 
            Rating/review data could not be scraped from Google Maps. 
            Using average rating from similar locations (category and hexagon averages) as fallback.
            For more accurate predictions, use "Manual Input" mode and provide actual rating/reviews.
            """)
        else:
            st.warning("""
            ⚠️ **Rating/Review Data Not Available**: 
            Google Maps loads this data via JavaScript, which our scraper cannot access. 
            **Solution**: Use "Manual Input" mode and copy the rating/reviews directly from Google Maps for more accurate predictions.
            """)
    
    # Analytics Section
    st.markdown("---")
    st.markdown("## 📊 Analytics & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Confidence Gauge - Show Beer Sales Potential confidence, not quantity confidence
        st.markdown("### 🎯 Beer Sales Potential Confidence")
        st.plotly_chart(create_confidence_gauge(beer_sales_confidence), width='stretch')
    
    with col2:
        # Features Chart
        features_chart = create_features_chart(all_features)
        if features_chart:
            st.plotly_chart(features_chart, width='stretch')
    
    # Quantity Prediction Explanation (if available)
    if quantity_pred and prediction_label == 'Beer Seller':
        st.markdown("### 📊 Quantity Prediction Explanation")
        quartile = quantity_pred.get('quartile', 0)
        quartile_label = quantity_pred.get('quartile_label', f'Q{quartile}')
        
        with st.expander(f"📊 How Quantity Prediction Works", expanded=False):
            st.markdown(f"""
            **Predicted Quartile**: {quartile_label}
            
            The quantity prediction model uses the **same features** as the binary classification model, but predicts 
            which **sales volume quartile** this outlet is likely to fall into:
            
            **Features Used:**
            - 📝 **Place Name (TF-IDF)**: ~9,000 text features from the name
            - ⭐ **Rating & Reviews**: Customer satisfaction indicators
            - 🏷️ **Category**: Location type (Restaurant, Bar, etc.)
            - 📍 **Location**: Latitude, Longitude, H3 Hexagon
            - 🏘️ **Ward & Province**: Administrative boundaries
            
            **How Quartiles Are Determined:**
            - The model was trained on outlets with known sales volumes
            - Outlets were divided into 4 quartiles based on actual sales volume
            - Q1 = Lowest 25%, Q2 = 25-50%, Q3 = 50-75%, Q4 = Highest 25%
            
            **What This Means:**
            - **Q4 (Highest)**: Top performers - prioritize these locations
            - **Q3**: Good performers - solid opportunities
            - **Q2**: Average performers - consider other factors
            - **Q1 (Lowest)**: Lower volume - may need support/marketing
            
            **Confidence**: {quantity_pred.get('confidence', 0)*100:.1f}% - This indicates how certain the model is about the quartile assignment.
            """)
    
    # Result Explanation
    st.markdown("### 💡 Prediction Explanation")
    # Pass beer_sales_confidence explicitly to avoid confusion
    result_with_confidence = result.copy()
    result_with_confidence['confidence'] = beer_sales_confidence
    result_with_confidence['confidence_percentage'] = f"{beer_sales_confidence*100:.2f}%"
    explanations = create_result_explanation(result_with_confidence, all_features)
    for exp in explanations:
        with st.expander(f"{exp['icon']} {exp['title']}", expanded=False):
            st.write(exp['text'])
    
    # Feature Distributions
    st.markdown("### 📈 Feature Distributions & Reference Ranges")
    st.markdown("""
    These charts show where your location's features fall compared to typical values for beer-selling outlets in Ho Chi Minh City.
    - **Green**: Value is in the optimal range
    - **Orange**: Value is within typical range
    - **Red**: Value is outside typical range
    - **Blue dashed line**: Typical/average value
    """)
    dist_charts = create_feature_distribution_charts(all_features)
    if dist_charts:
        # Display charts in a grid
        num_charts = len(dist_charts)
        if num_charts <= 2:
            cols = st.columns(num_charts)
            for idx, (feature_key, fig) in enumerate(dist_charts):
                with cols[idx]:
                    st.plotly_chart(fig, width='stretch')
        else:
            # For more charts, show 2 per row
            for i in range(0, num_charts, 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < num_charts:
                        with cols[j]:
                            st.plotly_chart(dist_charts[i + j][1], width='stretch')
    else:
        st.info("Feature distribution charts require numeric feature values. Some features may be missing (N/A).")
    
    # Detailed Features Table
    st.markdown("### 🔍 Detailed Features")
    
    # Convert all values to strings to avoid Arrow serialization issues
    def format_value(val):
        if val is None:
            return 'N/A'
        if isinstance(val, (int, float)):
            if isinstance(val, float):
                return f"{val:.4f}" if val != int(val) else str(int(val))
            return str(val)
        return str(val)
    
    # Create feature descriptions
    feature_descriptions = {
        "Average Rating": "Customer satisfaction score (1-5 stars)",
        "Reviews Number": "Total number of customer reviews",
        "Last Avg Rating": "Historical average rating (estimated)",
        "Last 1 Reviews": "Recent period reviews count (estimated: 30% of total)",
        "Last 2 Reviews": "Last 2 periods reviews count (estimated: 50% of total)",
        "Latitude": "GPS latitude coordinate",
        "Longitude": "GPS longitude coordinate",
        "Location Type": "Business category - strongly influences prediction",
        "Province": "Province name (default: Ho Chi Minh City)",
        "Ward": "Ward/district name for location context",
        "H3 Index": "Geospatial hexagon index - identifies area patterns",
        "Place Name": "Place name analyzed via TF-IDF (~9,000 text features)"
    }
    
    features_data = [
        {"Feature": "Average Rating", "Value": format_value(all_features.get('avg_rating')), "Description": feature_descriptions["Average Rating"]},
        {"Feature": "Reviews Number", "Value": format_value(all_features.get('reviews_number')), "Description": feature_descriptions["Reviews Number"]},
        {"Feature": "Last Avg Rating", "Value": format_value(all_features.get('last_avg_rating')), "Description": feature_descriptions["Last Avg Rating"]},
        {"Feature": "Last 1 Reviews", "Value": format_value(all_features.get('last_1_reviews_number')), "Description": feature_descriptions["Last 1 Reviews"]},
        {"Feature": "Last 2 Reviews", "Value": format_value(all_features.get('last_2_reviews_number')), "Description": feature_descriptions["Last 2 Reviews"]},
        {"Feature": "Latitude", "Value": format_value(all_features.get('latitude')), "Description": feature_descriptions["Latitude"]},
        {"Feature": "Longitude", "Value": format_value(all_features.get('longitude')), "Description": feature_descriptions["Longitude"]},
        {"Feature": "Location Type", "Value": format_value(all_features.get('location_type_resolved')), "Description": feature_descriptions["Location Type"]},
        {"Feature": "Province", "Value": format_value(all_features.get('province_name')), "Description": feature_descriptions["Province"]},
        {"Feature": "Ward", "Value": format_value(all_features.get('ward_name')), "Description": feature_descriptions["Ward"]},
        {"Feature": "H3 Index", "Value": format_value(all_features.get('idx_r9_hex')), "Description": feature_descriptions["H3 Index"]},
        {"Feature": "Place Name", "Value": format_value(all_features.get('name')), "Description": feature_descriptions["Place Name"]},
    ]
    
    features_df = pd.DataFrame(features_data)
    
    # Display with expandable descriptions
    st.dataframe(
        features_df[["Feature", "Value"]], 
        width='stretch', 
        hide_index=True
    )
    
    # Key Features Highlight Section
    st.markdown("#### 🔑 Key Feature Highlights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📝 Place Name (TF-IDF)**")
        name = all_features.get('name', 'N/A')
        tfidf_analysis = result.get('tfidf_analysis', {})
        important_terms = tfidf_analysis.get('important_terms', [])
        common_terms = tfidf_analysis.get('common_beer_terms_found', [])
        
        if important_terms or common_terms:
            # Dynamic description based on actual analysis
            terms_display = ', '.join([f'"{t}"' for t in (common_terms[:3] or important_terms[:3])])
            st.info(f'"{name}"\n\nAnalyzed as ~9,000 text features. Detected keywords: {terms_display}')
        else:
            st.info(f'"{name}"\n\nAnalyzed as ~9,000 text features. Keywords indicate business type.')
    
    with col2:
        st.markdown("**🏷️ Location Category**")
        category = format_value(all_features.get('location_type_resolved'))
        category_emoji = '🍽️' if 'restaurant' in str(category).lower() or 'quán' in str(category).lower() else '🏪'
        st.info(f'{category_emoji} **{category}**\n\nStrong predictor. Restaurants, bars, and cafes typically have higher beer sales potential.')
    
    with col3:
        st.markdown("**🔷 H3 Hexagon Index**")
        h3_idx = format_value(all_features.get('idx_r9_hex'))
        st.info(f'`{h3_idx}`\n\nGeospatial feature (~0.46 km² per hexagon). Identifies area patterns and commercial districts.')
    
    # Aggregated Features Section
    aggregated = result.get('aggregated_features', {})
    if aggregated:
        st.markdown("---")
        st.markdown("## 📊 Aggregated Statistics (From Training Data)")
        
        # Category Statistics
        category_features = aggregated.get('category_features')
        if category_features:
            st.markdown("### 🏷️ Category Statistics")
            
            # Explanation for low rates
            category_name = place_info.get('category', 'Category')
            beer_rate = category_features.get('beer_seller_percentage', 0)
            
            if category_name.lower() == 'restaurant' and beer_rate < 20:
                with st.expander("ℹ️ Why is the Restaurant beer seller rate lower than expected?", expanded=False):
                    st.markdown("""
                    **The "Restaurant" category is very broad** and includes many types:
                    
                    **High Beer Seller Rates:**
                    - 🍖 BBQ/Barbecue restaurants: ~20-30%
                    - 🍲 Hot pot restaurants: ~30%
                    - 🍺 Beer restaurants: ~23%
                    - 🍱 Korean BBQ: ~48%
                    - 🍣 Japanese restaurants: ~21%
                    
                    **Lower Beer Seller Rates:**
                    - 🍜 Pho restaurants: ~9% (many don't serve alcohol)
                    - 🍔 Fast food restaurants: ~3%
                    - 🥗 Health food/Vegan restaurants: ~1-3%
                    - 🍛 Casual eateries: Often don't serve beer
                    
                    **Why the overall rate is 12.6%:**
                    - The "Restaurant" category includes ALL restaurant types
                    - Many casual/fast-food restaurants don't sell beer
                    - Only labeled outlets are included in statistics
                    - The rate reflects actual market reality in Ho Chi Minh City
                    
                    **For your location:** Check the specific restaurant type/subcategory for more accurate expectations.
                    """)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Beer Seller Rate",
                    f"{beer_rate:.1f}%",
                    help="Percentage of outlets in this category that sell beer"
                )
            
            with col2:
                st.metric(
                    "Total Outlets",
                    f"{category_features.get('total_outlets', 0):,}",
                    help="Total number of outlets in this category in training data"
                )
            
            with col3:
                st.metric(
                    "Beer Sellers",
                    f"{category_features.get('beer_sellers', 0):,}",
                    help="Number of beer-selling outlets in this category"
                )
            
            with col4:
                avg_rating = category_features.get('avg_rating')
                if avg_rating:
                    st.metric(
                        "Avg Rating (Category)",
                        f"{avg_rating:.1f} ⭐",
                        help="Average rating for outlets in this category"
                    )
            
            # Category distribution chart
            fig_cat = go.Figure()
            beer_sellers = category_features.get('beer_sellers', 0)
            total = category_features.get('total_outlets', 0)
            non_beer_sellers = total - beer_sellers
            
            fig_cat.add_trace(go.Bar(
                x=['Beer Sellers', 'Non-Beer Sellers'],
                y=[beer_sellers, non_beer_sellers],
                marker_color=['#2ecc71', '#e74c3c'],
                text=[f"{beer_sellers:,}", f"{non_beer_sellers:,}"],
                textposition='auto'
            ))
            fig_cat.update_layout(
                title=f"Distribution in {category_name}",
                xaxis_title="Outlet Type",
                yaxis_title="Number of Outlets",
                height=300
            )
            st.plotly_chart(fig_cat, width='stretch')
            
            # Show comparison with overall rate
            overall_stats = aggregated.get('overall_stats', {})
            if overall_stats:
                overall_rate = overall_stats.get('overall_beer_seller_percentage', 0)
                comparison = beer_rate - overall_rate
                if abs(comparison) > 1:
                    if comparison > 0:
                        st.success(f"✅ This category's beer seller rate ({beer_rate:.1f}%) is **{comparison:.1f} percentage points higher** than the overall average ({overall_rate:.1f}%)")
                    else:
                        st.info(f"ℹ️ This category's beer seller rate ({beer_rate:.1f}%) is **{abs(comparison):.1f} percentage points lower** than the overall average ({overall_rate:.1f}%)")
            
            # Show related restaurant subcategories with higher rates (if Restaurant category)
            if category_name.lower() == 'restaurant' and beer_rate < 25:
                # Get all restaurant subcategories from aggregated stats
                all_cat_stats = aggregated.get('all_category_stats')
                if not all_cat_stats:
                    # Fallback: try to get from aggregated_features directly
                    all_cat_stats = {}
                
                restaurant_subcats = {
                    k: v for k, v in all_cat_stats.items() 
                    if 'restaurant' in k.lower() and k != 'Restaurant' and v.get('beer_seller_percentage', 0) > beer_rate
                }
                
                if restaurant_subcats:
                    # Sort by beer seller rate
                    sorted_subcats = sorted(
                        restaurant_subcats.items(), 
                        key=lambda x: x[1].get('beer_seller_percentage', 0), 
                        reverse=True
                    )[:5]  # Top 5
                    
                    with st.expander(f"🍽️ Related Restaurant Types with Higher Beer Seller Rates", expanded=False):
                        st.markdown(f"""
                        **Your location is categorized as "Restaurant" (general category).**
                        Here are restaurant **subcategories** that have higher beer seller rates:
                        """)
                        for subcat, subcat_data in sorted_subcats:
                            subcat_rate = subcat_data.get('beer_seller_percentage', 0)
                            subcat_outlets = subcat_data.get('total_outlets', 0)
                            st.markdown(f"""
                            - **{subcat}**: {subcat_rate:.1f}% ({subcat_outlets:,} outlets)
                            """)
                        st.markdown("""
                        **Note:** If your restaurant is a specific type (BBQ, Hot Pot, Korean BBQ, etc.), 
                        it may have a higher beer seller rate than the general "Restaurant" category.
                        """)
        
        # Hexagon Statistics
        hexagon_features = aggregated.get('hexagon_features')
        h3_hex = all_features.get('idx_r9_hex')
        
        # Also try to get from place_data if not in all_features
        if not h3_hex or h3_hex == 'N/A':
            # Try to calculate from coordinates if available
            lat = all_features.get('latitude')
            lon = all_features.get('longitude')
            if lat and lon and lat != 0 and lon != 0:
                try:
                    import h3
                    h3_hex = h3.latlng_to_cell(lat, lon, 9)
                except:
                    pass
        
        st.markdown("### 🔷 Hexagon (H3) Statistics")
        
        if h3_hex and h3_hex != 'N/A' and h3_hex is not None:
            st.info(f"**H3 Hexagon Index**: `{h3_hex}` (Area: ~0.46 km², Resolution 9)")
        
        if hexagon_features:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Beer Seller Rate (Hexagon)",
                    f"{hexagon_features.get('beer_seller_percentage', 0):.1f}%",
                    help="Percentage of outlets in this hexagon that sell beer"
                )
            
            with col2:
                st.metric(
                    "Total Outlets (Hexagon)",
                    f"{hexagon_features.get('total_outlets', 0):,}",
                    help="Total number of outlets in this hexagon area (~0.46 km²)"
                )
            
            with col3:
                st.metric(
                    "Beer Sellers (Hexagon)",
                    f"{hexagon_features.get('beer_sellers', 0):,}",
                    help="Number of beer-selling outlets in this hexagon"
                )
            
            with col4:
                avg_rating_hex = hexagon_features.get('avg_rating')
                if avg_rating_hex:
                    st.metric(
                        "Avg Rating (Hexagon)",
                        f"{avg_rating_hex:.1f} ⭐",
                        help="Average rating for outlets in this hexagon"
                    )
            
            # Hexagon comparison with overall
            overall_stats = aggregated.get('overall_stats', {})
            if overall_stats:
                st.markdown("#### 📈 Hexagon vs Overall Comparison")
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Bar(
                    name='This Hexagon',
                    x=['Beer Seller Rate'],
                    y=[hexagon_features.get('beer_seller_percentage', 0)],
                    marker_color='#3498db',
                    text=[f"{hexagon_features.get('beer_seller_percentage', 0):.1f}%"],
                    textposition='auto'
                ))
                fig_comp.add_trace(go.Bar(
                    name='Overall Average',
                    x=['Beer Seller Rate'],
                    y=[overall_stats.get('overall_beer_seller_percentage', 0)],
                    marker_color='#95a5a6',
                    text=[f"{overall_stats.get('overall_beer_seller_percentage', 0):.1f}%"],
                    textposition='auto'
                ))
                fig_comp.update_layout(
                    title="How does this hexagon compare to overall?",
                    yaxis_title="Beer Seller Rate (%)",
                    height=300,
                    barmode='group'
                )
                st.plotly_chart(fig_comp, width='stretch')
        else:
            if h3_hex and h3_hex != 'N/A':
                st.warning(f"⚠️ No aggregated statistics available for hexagon `{h3_hex}`. This hexagon may not be in the training data.")
            else:
                st.info("ℹ️ H3 Hexagon index not available. Coordinates may be missing.")
        
        # Ward Statistics
        ward_features = aggregated.get('ward_features')
        if ward_features:
            st.markdown("### 🏘️ Ward Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Beer Seller Rate (Ward)",
                    f"{ward_features.get('beer_seller_percentage', 0):.1f}%"
                )
            
            with col2:
                st.metric(
                    "Total Outlets (Ward)",
                    f"{ward_features.get('total_outlets', 0):,}"
                )
            
            with col3:
                st.metric(
                    "Beer Sellers (Ward)",
                    f"{ward_features.get('beer_sellers', 0):,}"
                )
        
        # Overall Statistics
        overall_stats = aggregated.get('overall_stats', {})
        if overall_stats:
            st.markdown("### 📊 Overall Training Data Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Overall Beer Seller Rate",
                    f"{overall_stats.get('overall_beer_seller_percentage', 0):.1f}%"
                )
            
            with col2:
                st.metric(
                    "Total Outlets (Training)",
                    f"{overall_stats.get('total_outlets', 0):,}"
                )
            
            with col3:
                st.metric(
                    "Total Beer Sellers (Training)",
                    f"{overall_stats.get('total_beer_sellers', 0):,}"
                )
    
    # Location Map
    if all_features.get('latitude') and all_features.get('longitude'):
        st.markdown("---")
        st.markdown("### 🗺️ Location Map")
        map_df = pd.DataFrame({
            'lat': [all_features.get('latitude')],
            'lon': [all_features.get('longitude')],
            'name': [place_info.get('name', 'Location')]
        })
        st.map(map_df, zoom=15)
    
    # Add to history
    st.session_state.prediction_history.append({
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'place_name': place_info.get('name', 'Unknown'),
        'prediction': prediction_label,
        'confidence': beer_sales_confidence,
        'risk_level': risk_level
    })


def main():
    """Main Streamlit app"""
    # Header with Heineken Logo
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        try:
            logo_path = Path(__file__).parent / "heineken_logo.svg"
            if logo_path.exists():
                st.image(str(logo_path), use_container_width=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem 0;">
                    <h1 style="color: #00A651; font-size: 3rem; margin: 0;">HEINEKEN</h1>
                    <p style="color: #666; font-size: 1.2rem; margin: 0.5rem 0;">Beer Sales Potential Predictor</p>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <h1 style="color: #00A651; font-size: 3rem; margin: 0;">HEINEKEN</h1>
                <p style="color: #666; font-size: 1.2rem; margin: 0.5rem 0;">Beer Sales Potential Predictor</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        Predict the beer-selling potential of locations in Ho Chi Minh City using AI/ML models.
        Enter a Google Maps URL to get started.
    </div>
    """, unsafe_allow_html=True)
    
    # Check API health
    is_healthy, health_info = check_api_health(API_URL)
    
    if not is_healthy:
        st.error(f"❌ Cannot connect to API at {API_URL}")
        st.info("💡 Make sure the API is running. Start it with: `python main.py`")
        return
    
    # Show API status
    with st.sidebar:
        st.success("✅ API Connected")
        if health_info and health_info.get('model_info'):
            model_info = health_info['model_info']
            st.metric("Model AUC", f"{model_info.get('test_auc', 0):.4f}")
            st.metric("Model Accuracy", f"{model_info.get('test_accuracy', 0):.4f}")
            st.metric("Features", model_info.get('num_features', 0))
    
    # Info about scraping
    with st.expander("ℹ️ Why can't we scrape ratings/reviews?", expanded=False):
        st.markdown("""
        **The Problem:**
        - Google Maps loads rating and review data via JavaScript **after** the page loads
        - Our API makes simple HTTP requests that only get the initial HTML
        - JavaScript-rendered content is not available in the HTML response
        
        **Solutions:**
        1. ✅ **Use Manual Input mode** (Recommended) - Copy data directly from Google Maps
        2. ✅ **Use Google Places API** - Requires API key but provides reliable data
        3. ⚠️ **Accept defaults** - Model can still predict with location and category data
        
        **What we CAN extract:**
        - ✅ Place name, coordinates (from URL)
        - ✅ Location type/category (sometimes)
        - ✅ Address (sometimes)
        - ⚠️ Rating/Reviews (often fails due to JavaScript)
        """)
    
    # Main input section
    st.markdown("## 🔍 Predict Beer Sales Potential")
    
    # Input mode selection
    input_mode = st.radio(
        "Input Mode",
        ["Auto Scrape (from URL)", "Manual Input"],
        horizontal=True,
        help="Manual Input mode is recommended for accurate results when scraping fails"
    )
    
    if input_mode == "Auto Scrape (from URL)":
        google_maps_url = st.text_input(
            "Google Maps URL",
            placeholder="https://www.google.com/maps/place/...",
            help="Paste a Google Maps place URL here"
        )
        
        if st.button("🔮 Predict", type="primary", use_container_width=True):
            if not google_maps_url:
                st.warning("Please enter a Google Maps URL")
            else:
                with st.spinner("🔄 Analyzing place and making prediction..."):
                    result = predict_from_url(API_URL, google_maps_url)
                    if result:
                        display_prediction_result(result)
    
    else:  # Manual Input
        google_maps_url = st.text_input(
            "Google Maps URL",
            placeholder="https://www.google.com/maps/place/...",
            help="Paste a Google Maps place URL here"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            rating = st.number_input(
                "Rating (0-5)",
                min_value=0.0,
                max_value=5.0,
                value=4.0,
                step=0.1,
                help="Average rating from Google Maps"
            )
            reviews = st.number_input(
                "Number of Reviews",
                min_value=0,
                value=100,
                step=1,
                help="Total number of reviews"
            )
        
        with col2:
            category = st.text_input(
                "Category",
                placeholder="Restaurant, Cafe, Bar, etc.",
                help="Business category"
            )
            address = st.text_area(
                "Address",
                placeholder="Full address from Google Maps",
                help="Complete address"
            )
        
        if st.button("🔮 Predict", type="primary", use_container_width=True):
            if not google_maps_url:
                st.warning("Please enter a Google Maps URL")
            else:
                with st.spinner("🔄 Making prediction..."):
                    result = predict_manual(
                        API_URL,
                        google_maps_url,
                        rating=rating if rating > 0 else None,
                        reviews=int(reviews) if reviews > 0 else None,
                        category=category if category else None,
                        address=address if address else None
                    )
                    if result:
                        display_prediction_result(result)
    
    # Prediction History
    if st.session_state.prediction_history:
        st.markdown("---")
        st.markdown("## 📜 Prediction History")
        history_df = pd.DataFrame(st.session_state.prediction_history)
        st.dataframe(history_df, width='stretch', hide_index=True)
        
        if st.button("Clear History"):
            st.session_state.prediction_history = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; padding: 2rem;">
        <p>Heineken Beer Sales Potential Predictor - Powered by LightGBM ML Model</p>
        <p>Model Performance: AUC 0.8676 | Accuracy 82.62%</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

