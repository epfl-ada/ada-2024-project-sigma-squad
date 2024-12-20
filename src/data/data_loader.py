import pandas as pd

# The Oscar Award Dataset (https://www.kaggle.com/datasets/unanimad/the-oscar-award):

def load_oscars_data():
    """
    Loads and processes the Oscars dataset.

    Reads the Oscars dataset, renames relevant columns, converts movie names 
    to lowercase, and replaces spaces with underscores. Aggregates nominations 
    and wins by movie name.

    Returns:
        pd.DataFrame: A DataFrame containing processed Oscars data.
    """

    oscars = pd.read_csv('data/the_oscar_award.csv')
    oscars.rename(columns={'year_film': 'Movie release date'}, inplace=True)
    oscars.rename(columns={'film': 'movie_name'}, inplace=True)
    oscars['movie_name'] = oscars['movie_name'].str.lower().str.replace(' ', '_')

    oscars_to_merge = oscars.groupby(['movie_name'], as_index=False).agg({
        'Movie release date': 'first',
        'category': lambda x: ', '.join(f"{cat}: {name}" for cat, name in zip(x, oscars.loc[x.index, 'name'])),
        'winner': lambda x: ', '.join(oscars.loc[x.index, 'name'][oscars.loc[x.index, 'winner']]),
        'category': 'count'
    }).rename(columns={'category': 'num_nominations'})

    return oscars_to_merge


# TMDb Movie Dataset (https://github.com/danielgrijalva/movie-stats):

def load_movie_stats():
    """
    Loads and processes the TMDb movie dataset.

    Reads the TMDb movie dataset, renames relevant columns, normalizes movie 
    names by converting them to lowercase and replacing spaces with underscores. 
    Converts the release year to datetime format and extracts only the year.

    Returns:
        pd.DataFrame: A DataFrame containing processed TMDb movie data.
    """

    movie_stats = pd.read_csv('data/movie_stats.csv')
    movie_stats.rename(columns={'name': 'movie_name'}, inplace=True)
    movie_stats.rename(columns={'year': 'Movie release date'}, inplace=True)
    movie_stats['movie_name'] = movie_stats['movie_name'].str.lower().str.replace(' ', '_')
    movie_stats['Movie release date'] = movie_stats['Movie release date'].apply(convert_to_datetime)
    movie_stats['Movie release date'] = movie_stats['Movie release date'].dt.year

    return movie_stats


# CMU Movie Dataset (http://www.cs.cmu.edu/~ark/personas/):

def load_original_data():
    """
    Loads and processes the CMU Movie dataset.

    Reads the CMU Movie dataset, renames relevant columns, normalizes movie 
    names by converting them to lowercase and replacing spaces with underscores.
    Converts the release date to datetime format and extracts only the year.

    Returns:
        pd.DataFrame: A DataFrame containing processed CMU Movie data.
    """
    
    original_data = pd.read_csv('data/movie.metadata.tsv', sep='\t', names= ['Wikipedia movie ID', 'Freebase movie ID', 'Movie name', 'Movie release date', 'Movie box office revenue', 'Movie runtime', 'Movie languages', 'Movie countries', 'Movie genres'])
    original_data.rename(columns={'Movie name': 'movie_name'}, inplace=True)
    original_data['movie_name'] = original_data['movie_name'].str.lower().str.replace(' ', '_')
    original_data['Movie release date'] = original_data['Movie release date'].apply(convert_to_datetime)
    original_data['Movie release date'] = original_data['Movie release date'].dt.year
    
    return original_data


# Freebase Character Metadataset (http://www.cs.cmu.edu/~ark/personas/):

def load_character_data():
    """
    Loads character data from the charachter.metadata TSV file (2012 dump of Freebase).

    Returns:
        pandas.DataFrame: DataFrame containing the character data.
    """
    character_data = pd.read_csv('data/character.metadata.tsv', sep='\t', names= ['Wikipedia movie ID', 'Freebase movie ID', 'Movie release date', 'Character name', 'Actor date of birth', 'Actor gender', 
                                 'Actor height', 'Actor ethnicity', 'Actor name', 'Actor age at movie release', 'Freebase character/actor map ID', 'Freebase character ID', 'Freebase actor ID'])
    return character_data


def load_actor_data_for_analysis():
    """
    Loads the pre-completed actor data for analysis.
    Converts columns containing floats to int.

    Returns:
        pandas.DataFrame: DataFrame containing the actor data for analysis.
    """

    actor_df = pd.read_csv('data/actor_data_for_analysis.csv', index_col=0)
    actor_df['Age at First Release'] = actor_df['Age at First Release'].astype('Int64')
    actor_df['Number of Children'] = actor_df['Number of Children'].astype('Int64')
    actor_df['Birth Year'] = actor_df['Birth Year'].astype('Int64')

    return actor_df


def convert_to_datetime(date):
    """
    Converts a date to datetime format. 

    Checks if the input date is a 4-digit year; if so, converts it to a 
    full date format ('yyyy-01-01'). Otherwise, attempts to convert it 
    to datetime format. Returns NaT for invalid formats.

    Args:
        date (str or int): The date to be converted.

    Returns:
        pd.Timestamp: The converted date as a datetime object
    """

    if len(str(date)) == 4 and str(date).isdigit():  # Only year (e.g., 1988)
        return pd.to_datetime(str(date) + '-01-01')
    else:
        return pd.to_datetime(date, errors='coerce')  # Convert if it's in a full date format
