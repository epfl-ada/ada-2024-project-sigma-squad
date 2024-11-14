import pandas as pd
import sys
import os

sys.path.append(os.path.abspath('src/data'))
from data_loader import load_oscars_data, load_movie_stats, load_original_data


def merge_data():
    """
    Merges data from all three datasets into a single DataFrame.

    This function merges data from the Oscars, TMDb, and CMU Movie datasets
    on common columns ('movie_name' and 'Movie release date').

    Returns:
        pd.DataFrame: A DataFrame containing merged data from all three datasets.
    """

    oscars_data = load_oscars_data()
    movie_stats = load_movie_stats()
    original_data = load_original_data()

    # merge datasets
    merged_data = pd.merge(original_data, movie_stats, on=['movie_name', 'Movie release date'], how='left')
    final_merged_data = merged_data.merge(oscars_data, on=['movie_name', 'Movie release date'], how='left')
    
    return final_merged_data


def raw_data():
    """
    Cleans the merged movie dataset by dropping irrelevant columns and renaming
    columns for consistency.

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis.
    """

    merged_data = merge_data()

    # Drop irrelevant columns
    merged_data.drop(columns=['Wikipedia movie ID', 'genre', 'released', 'country', 'runtime', 'rating', 'writer'], inplace=True)

    # Rename columns for consistency
    merged_data.rename(columns={
        'movie_name': 'Movie name',
        'score': 'Review score',
        'votes': 'Movie votes',
        'director': 'Movie director',
        'star': 'Movie star',
        'budget': 'Movie budget',
        'gross': 'Movie gross',
        'company': 'Movie company',
        'num_nominations': 'Number of nomination',
        'winner': 'Nomination winner'
    }, inplace=True)

    # Change type
    merged_data['Movie release date'] = merged_data['Movie release date'].astype('Int64')

    # Convert genres and countries to comma-separated strings
    merged_data['Movie genres'] = merged_data['Movie genres'].apply(eval).apply(get_key_values)
    merged_data['Movie countries'] = merged_data['Movie countries'].apply(eval).apply(get_key_values)

    return merged_data


def clean_data(raw_data):
    # Drop rows with NA values in essential columns
    clean_data = raw_data.dropna(subset=['Movie box office revenue', 'Movie budget', 'Review score', 'Movie votes']).copy()

    return clean_data


def get_key_values(x):
    """
    Converts values of a dictionary to a comma-separated string.

    Args:
        x (dict): A dictionary with string values.

    Returns:
        str: A comma-separated string of all values in the dictionary.
    """

    return ', '.join(x.values())




if __name__ == "__main__":
    df = raw_data()
    print(clean_data(df).head)