import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from src.constants import ETHNICITY_MAPPING


def encode_categorical(df, columns):
    """
    Encodes categorical features in the given DataFrame using one-hot encoding.
    """
    return pd.get_dummies(df, columns=columns)


def display_correlation(df, plot=False):
    """
    Calculate and display the correlation of all features with the 'Success Score' in the given DataFrame.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    ## Correlation of Sucess score with other features
    corr = df.corr()
    corr_success = corr['Success Score']
    corr_success = corr_success.sort_values(ascending=False)
    corr_success = corr_success.drop('Success Score')
    return corr_success

def ethnicity_to_group(df):
    """
    Maps the 'Ethnicity' column of the given DataFrame to a predefined set of groups.
    """
    df.Ethnicity = df.Ethnicity.map(ETHNICITY_MAPPING)
    df = df.dropna(subset=['Ethnicity'])
    return df


