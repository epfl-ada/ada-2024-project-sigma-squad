import pandas as pd
from ..engines import converter, university_matcher, spider
from src.constants import REGION_LIST
from tqdm import tqdm


def scrape_actor_data(actor_df):
    """
    This function activates the actor data scraping process.

    Parameters:
    actor_df: DataFrame containing the actor information.
    """

    print('Collecting actor information...')
    spider.run_scraping(actor_df)
    return


def convert_ethnicity_ids(actor_df):
    """
    This function starts the mapping of ethnicity entity IDs to their corresponding ethnicity names.

    Parameters:
    actor_df: The DataFrame containing the actor data.
    """

    tqdm.pandas() # for progress_apply
    print('Converting ethnicity entity IDs...')
    actor_df.loc[:, 'Ethnicity'] = actor_df['Ethnicity'].progress_apply(converter.get_ethnicity)
    return


def match_universities(actor_df):
    """
    This function starts the university matching process.

    Parameters:
    actor_df: The DataFrame containing the actor data.
    """
    university_matcher.clean_universities(actor_df)
    return


def clean_actor_data(actor_df):
    """
    Cleans and processes the actor data, to be ready for analysis.

    Parameters:
    actor_df: The DataFrame containing the actor data.
    """

    actor_df.rename(columns={'Actor date of birth': 'Date of Birth',
                             'Actor gender': 'Gender',
                             'Actor height': 'Height',
                             'Actor ethnicity': 'Ethnicity',
                             'Actor age at movie release': 'Age at First Release',
                             'Actor Score Index': 'Success Score'},
                    inplace=True)
    
    convert_ethnicity_ids(actor_df)
    separate_dob_into_year_month(actor_df)
    match_universities(actor_df)
    groupby_region(actor_df)

    # Changes Theater values to boolean
    actor_df['Theater'] = actor_df['Theater'].apply(lambda x: True if (x == 'Yes') else False)

    # Recast values to integers
    actor_df['Age at First Release'] = actor_df['Age at First Release'].astype('Int64')
    return


def separate_dob_into_year_month(actor_df):
    """
    Separates the 'Date of Birth' column into 'Birth Year' and 'Birth Month' columns, using datetime format.

    Parameters:
    actor_df: The DataFrame containing the actor data.
    Parameters:
    actor_df: The DataFrame containing the actor data.
    """

    actor_df['Date of Birth'] = pd.to_datetime(actor_df['Date of Birth'], errors='coerce')
    actor_df['Birth Year'] = actor_df['Date of Birth'].dt.year.astype('Int64')
    actor_df['Birth Month'] = actor_df['Date of Birth'].dt.month_name()
    actor_df.drop(columns='Date of Birth', inplace=True)
    return


def groupby_region(actor_df):
    """
    Groups actors by their birth region based on their birth city and citizenship.
    The regions are: USA, United Kingdom, Europe and Rest of World.

    Parameters:
    actor_df: The DataFrame containing the actor data.
    """

    regions = ['USA', 'United Kingdom', 'Europe', 'nan']

    actor_df['Birth Region'] = actor_df['Birth City'].astype(str)

    for birth_city, region in REGION_LIST:
        actor_df.loc[actor_df['Birth Region'].str.contains(birth_city, case=False), 'Birth Region'] = region

    actor_df['Birth Region'] = actor_df['Birth Region'].apply(lambda x: x if x in regions else 'Rest of World')

    # Fill in missing values with USA if citizenship is USA
    actor_df.loc[actor_df['Birth Region'].str.contains('nan') & actor_df['Citizenship'].notna(), 'Birth City'] = 'USA'

    actor_df.drop(columns=['Birth City', 'Citizenship'], inplace=True)
    return
