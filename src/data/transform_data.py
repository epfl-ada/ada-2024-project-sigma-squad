import pandas as pd
from data_loader import load_oscars_data, load_movie_stats, load_original_data


def merge_data():
    """
    Merges data from all three datasets into a single DataFrame.

    This function merges data from the Oscars, TMDb, and CMU Movie datasets
    on common columns ('movie_name' and 'Movie release date').

    Returns:
        pd.DataFrame: A DataFrame containing merged data from all three datasets.
    """

    oscars_to_merge = load_oscars_data()
    movie_stats = load_movie_stats()
    original_data = load_original_data()

    # merge datasets
    merged = pd.merge(original_data, movie_stats, on=['movie_name', 'Movie release date'], how='left')
    final_merged_data = merged.merge(oscars_to_merge, on=['movie_name', 'Movie release date'], how='left')
    
    return final_merged_data


def clean_data():
    """
    Cleans the merged movie dataset by dropping irrelevant columns, renaming
    columns for consistency, and handling missing values.

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis.
    """

    final_merged_data = merge_data()

    # Drop irrelevant columns
    final_merged_data.drop(columns=['Wikipedia movie ID', 'genre', 'released', 'country', 'runtime', 'rating', 'writer'], inplace=True)

    # Rename columns for consistency
    final_merged_data.rename(columns={
        'movie_name': 'Movie name',
        'score': 'Movie score',
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
    final_merged_data['Movie release date'] = final_merged_data['Movie release date'].astype('Int64')

    # Convert genres and countries to comma-separated strings
    final_merged_data['Movie genres'] = final_merged_data['Movie genres'].apply(eval).apply(get_key_values)
    final_merged_data['Movie countries'] = final_merged_data['Movie countries'].apply(eval).apply(get_key_values)

    # Drop rows with NA values in essential columns
    clean_df = final_merged_data.dropna(subset=['Movie box office revenue', 'Movie budget', 'Movie score', 'Movie votes']).copy()

    return clean_df


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
    print(clean_data().head)