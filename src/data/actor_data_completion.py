import pandas as pd
from ..converter import converter
from ..webscraping import spider
from tqdm import tqdm


def scrape_actor_data(actor_df):

    print('Scraping actor data...')
    spider.run_scraping(actor_df)
    return


def convert_ethnicity_ids(actor_df):

    tqdm.pandas() # for progress_apply
    print('Converting ethnicity...')
    actor_df.loc[:, 'Ethnicity'] = actor_df['Ethnicity'].progress_apply(converter.get_ethnicity)
    return


def separate_dob_into_year_month(actor_df):

    actor_df['Date of Birth'] = pd.to_datetime(actor_df['Date of Birth'], errors='coerce')
    actor_df['Birth Year'] = actor_df['Date of Birth'].dt.year.astype('Int64')
    actor_df['Birth Month'] = actor_df['Date of Birth'].dt.month_name()
    actor_df.drop(columns='Date of Birth', inplace=True)

    return


def clean_actor_data(actor_df):

    actor_df.rename(columns={'Actor date of birth': 'Date of Birth',
                             'Actor gender': 'Gender',
                             'Actor ethnicity': 'Ethnicity',
                             'Actor age at movie release': 'Age at First Release',
                             'Actor Score Index': 'Success Score'},
                    inplace=True)
    
    convert_ethnicity_ids(actor_df)
    separate_dob_into_year_month(actor_df)

    #TODO: ...

    return
