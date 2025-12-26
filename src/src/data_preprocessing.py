"""
Data preprocessing utilities for the PCA-Based Manufacturing Analytics Dashboard.

This module includes functions for:
- Loading data
- Cleaning and preparing variables
- Handling missing values
- Scaling numeric features
- Saving processed outputs
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_data(path):
    """Load CSV data from the given file path."""
    return pd.read_csv(path)


def clean_column_names(df):
    """Standardise column names for consistency."""
    df.columns = (
        df.columns.str.strip()
                  .str.replace(" ", "_")
                  .str.replace("-", "_")
    )
    return df


def handle_missing_values(df):
    """Fill or remove missing values."""
    return df.fillna(method="ffill").fillna(method="bfill")


def scale_numeric_features(df, numeric_cols):
    """
    Standardise numeric variables for PCA.
    Returns scaled array and fitted scaler.
    """
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[numeric_cols])
    return scaled, scaler


def save_processed_data(df, path):
    """Save cleaned dataset to the processed folder."""
    df.to_csv(path, index=False)
