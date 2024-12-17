from ..converter import converter
from ..webscraping import spider
from tqdm import tqdm


def convert_ethnicity_ids(actor_df):

    tqdm.pandas() # for progress_apply
    print('Converting ethnicity...')
    actor_df.loc[:, 'Actor ethnicity'] = actor_df['Actor ethnicity'].progress_apply(converter.get_ethnicity)
    return


def complete_actor_data(actor_df):

    print('Completing actor data...')
    spider.run_scraping(actor_df)
    return


def clean_actor_data(actor_df):
    
    #placeholder
    return
