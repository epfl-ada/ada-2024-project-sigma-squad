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


# CMU Movie Dataset:

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




if __name__ == "__main__":
    print(load_oscars_data().head())
    print()
    print(load_movie_stats().head())
    print()
    print(load_original_data().head())