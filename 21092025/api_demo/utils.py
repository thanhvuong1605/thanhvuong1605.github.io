"""
Shared utilities for beer sales prediction
Must be imported by both training notebook and API to ensure pickle compatibility
"""


def simple_tokenizer(x):
    """
    Simple tokenizer for TF-IDF
    This function must be defined at module level for pickle compatibility
    """
    return str(x).lower().split()



