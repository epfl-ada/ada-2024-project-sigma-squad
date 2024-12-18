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


def groupby_region(actor_df):
    regions = ['USA', 'United Kingdom', 'Europe', 'nan']
    region_list = [('US', 'USA'),
        ('United States', 'USA'),
        ('Texas', 'USA'),
        ('South Carolina', 'USA'),
        ('Michigan', 'USA'),
        ('Illinois', 'USA'),
        ('Alabama', 'USA'),
        ('Los Angeles', 'USA'),
        ('Indianapolis', 'USA'),
        ('New York', 'USA'),
        ('Virginia', 'USA'),
        ('New Jersey', 'USA'),
        ('Brooklyn', 'USA'),
        ('Tennessee', 'USA'),
        ('Pennsylvania', 'USA'),
        ('Chicago', 'USA'),
        ('Nebraska', 'USA'),
        ('Florida', 'USA'),
        ('Ohio', 'USA'),
        ('Scotland', 'United Kingdom'),
        ('England', 'United Kingdom'),
        ('Wales', 'United Kingdom'),
        ('Ireland', 'United Kingdom'),
        ('Berkshire', 'United Kingdom'),
        ('Frankfurt', 'Europe'),
        ('Germany', 'Europe'),
        ('Spain', 'Europe'),
        ('Netherlands', 'Europe'),
        ('Amsterdam', 'Europe'),
        ('France', 'Europe'),
        ('Iceland', 'Europe'),
        ('Italy', 'Europe'),
        ('Bulgaria', 'Europe'),
        ('Sweden', 'Europe'),
        ('Bosnia', 'Europe'),
        ('Croatia', 'Europe'),
        ('Denmark', 'Europe'),
        ('Slovakia', 'Europe'),]

    actor_df['Birth Region'] = actor_df['Birth City'].astype(str)

    for birth_city, region in region_list:
        actor_df.loc[actor_df['Birth Region'].str.contains(birth_city, case=False), 'Birth Region'] = region

    actor_df['Birth Region'] = actor_df['Birth Region'].apply(lambda x: x if x in regions else 'Rest of World')

    # Fill in missing values with USA if citizenship is USA
    actor_df.loc[actor_df['Birth Region'].str.contains('nan') & actor_df['Citizenship'].notna(), 'Birth City'] = 'USA'

    #actor_df.drop(columns=['Birth City', 'Citizenship'], inplace=True)
        
    return


def clean_actor_data(actor_df):

    actor_df.rename(columns={'Actor date of birth': 'Date of Birth',
                             'Actor gender': 'Gender',
                             'Actor height': 'Height',
                             'Actor ethnicity': 'Ethnicity',
                             'Actor age at movie release': 'Age at First Release',
                             'Actor Score Index': 'Success Score'},
                    inplace=True)
    
    convert_ethnicity_ids(actor_df)
    separate_dob_into_year_month(actor_df)
    groupby_region(actor_df)

    actor_df['Age at First Release'] = actor_df['Age at First Release'].astype('Int64')
    actor_df['Theater'] = actor_df['Theater'].apply(lambda x: True if (x == 'Yes') else False)


    #TODO: ...

    return
