import pandas as pd
from ..converter import converter
from ..webscraping import spider
from tqdm import tqdm
from rapidfuzz import process


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

def match_universities(uni_name, qs_uni):
    if not isinstance(uni_name, str):  # Check if the value is NaN
        return None
    result = process.extractOne(uni_name, qs_uni)
    if result:
        match, score, _ = result  # Unpack match, score, and index
        return match if score > 88 else None  # Return match only if confidence > 80
    return None

def clean_rank(rank):
    if rank == 'Not Ranked':
        return 'Not Ranked'
    if '=' in rank:
        return int(rank.replace('=',''))
    if '-' in rank:
        return int(rank.split('-')[0].strip())
    if '+' in rank:
        return int(rank.split('+')[0].strip())
    else:
        return int(rank)

def contains_keyword(column, keyword):
    return column.str.contains(keyword, case=False, na=False).astype(int)

def clean_universities(actor_df: pd.DataFrame):

    # Load the values of the QS University Rankings 2024
    rankings = pd.read_csv('data/2024_QS_World_University_Rankings_csv', header=0)
    
    # Do a first round of matching the institution names to the universities found through scraping
    qs_uni_names = rankings['Institution Name'].to_list()
    actor_df['Matched Uni'] = actor_df['University'].apply(lambda x: match_universities(x, qs_uni_names))

    # Replace the original values of the university with those found through matching, allows to attach rank from QS
    actor_df['University'] = actor_df.apply(
    lambda row: row['Matched Uni'] if pd.notna(row['Matched Uni']) else row['University'], axis = 1
    )

    # Create binary indicator of whether or not a match was found
    actor_df['found_match'] = actor_df.apply(lambda row: True if pd.notna(row['Matched Uni']) else False, axis=1)

    # Remove the now unnecessary Matched Uni column
    actor_df.drop(columns=['Matched Uni'], inplace=True)

    # Replace all values containing 'High School' with 'None'
    actor_df.loc[
        actor_df['University'].str.contains('high school', case=False, na=False),
        'University'
    ] = None

    # Replace all mentions of 'Academy Award' by None
    actor_df.loc[
        actor_df['University'].str.contains('Academy Award', case=False, na=False),
        'University'
    ] = None

    list_of_cases = [
        ('drama','Specialised Drama School'),
        ('dramatic','Specialised Drama School'),
        ('theater','Specialised Drama School'),
        ('theatre','Specialised Drama School'),
        ('performing arts','Specialised Drama School'),
        ('acting','Specialised Acting School'),
        ('film','Specialised Acting School'),
        ('oxford','University of Oxford'),
        ('college cambridge', 'University of Cambridge'),
        ('trinity hall', 'University of Cambridge'),
        ('University of California Los Angeles', "University of California, Los Angeles (UCLA)"),
        ('UCLA', "University of California, Los Angeles (UCLA)"),
        ('University of California Santa Barbara', "University of California, Santa Barbara (UCSB)"),
        ('University College London', 'UCL'),
        ('Kings College London', "King's College London"),
        ('University of Toronto', 'University of Toronto'),
        ('University of Georgia', 'The University of Georgia'),
        ('Harvard', 'University of Harvard'),
        ('University of Missouri', 'University of Missouri'),
        ('University of North Carolina', 'University of North Carolina'),
        ('San Diego State', 'San Diego State University'),
        ('University of Texas', 'University of Texas'),
        ('University of Alabama', 'University of Alabama'),
        ('University of Michigan', 'University of Michigan-Ann Arbor'),
        ('Texas AM', 'Texas A&M University'),
        ('Fordham', 'Fordham University'),
        ('Rutgers', 'Rutgers University–New Brunswick'),
        ('vassar', 'Vassar College'),
        ('Music', 'Specialised Music School'),
        ('Conservatory','Specialised Music School'),
        ('Conservatoire', 'Specialised Music School'),
        ('Juilliard', 'Specialised Music School'),
        ('ballet', 'Specialised Dance School'),
        ('dance', 'Specialised Dance School'),
        ('art', 'Specialised Arts School'),
        ('arts', 'Specialised Arts School')
    ]

    for (word, school) in list_of_cases:
        actor_df.loc[
            actor_df['University'].str.contains(word, case=False, na=False),
            'University'
        ] = school
    
    # Second round of matching
    actor_df['Matched Uni'] = actor_df['University'].apply(lambda x: match_universities(x, qs_uni_names))

    actor_df['University'] = actor_df.apply(
        lambda row: row['Matched Uni'] if pd.notna(row['Matched Uni']) else row['University'], axis = 1
    )

    actor_df['found_match'] = actor_df.apply(lambda row: True if pd.notna(row['Matched Uni']) else False, axis=1)

    actor_df.drop(columns=['Matched Uni'], inplace=True)

    # Specify those that did not go to uni
    actor_df['University'] = actor_df['University'].fillna('Did not go')

    # Update 'University' where conditions are met
    actor_df.loc[
        (actor_df['found_match'] == False) &  # Check if 'found_match' is False
        (~(actor_df['University'] == 'Did not go')) & # Check if empty
        (~actor_df['University'].str.lower().str.startswith('specialised', na=False)) &  # Does NOT start with 'specialized'
        (~actor_df['University'].str.lower().str.startswith('vassar', na=False)),  # Does NOT start with 'vassar'
        'University'
    ] = 'sub 1500 school'

    # Reset index to safely preserve 'actor_name' during merge
    show_data_reset = actor_df.reset_index()

    # Perform the left join
    show_data_reset = show_data_reset.merge(
        rankings[['Institution Name', '2024 QS World University Rankings']],  # Select columns from rankings
        left_on='University',                    # Column in show_data
        right_on='Institution Name',             # Column in rankings
        how='left'                               # Left join keeps all rows in show_data
    )

    # Add 'uni_rank' while keeping other columns intact
    show_data_reset['uni_rank'] = show_data_reset['2024 QS World University Rankings']  # Copy Rank to uni_rank

    # Drop redundant 'Institution Name' and 'Rank' columns if needed
    show_data_reset = show_data_reset.drop(columns=['Institution Name', '2024 QS World University Rankings'], errors='ignore')

    # Fill missing 'uni_rank' for unmatched universities with 'Not Ranked'
    show_data_reset['uni_rank'] = show_data_reset['uni_rank'].fillna('Not Ranked')

    # Set 'actor_name' back as the index
    actor_df = show_data_reset.set_index('Actor name')

    # Get rid of the now useless found_match column
    actor_df.drop(columns=['found_match'], inplace=True)

    actor_df['uni_rank'] = actor_df['uni_rank'].apply(clean_rank)

    # Create a binary column: 1 if 'uni_rank' is numeric, 0 if 'Not Ranked'
    actor_df['Ranked Uni'] = actor_df['uni_rank'].apply(lambda x: 1 if isinstance(x, int) else 0)

    # Replace 'Not Ranked' with a placeholder of 3000 (very large)
    actor_df['Usable Uni Rank'] = actor_df['uni_rank'].apply(lambda x: x if isinstance(x, int) else 3000)

    # Create binary columns of whether or not the actor went to a specialised school
    actor_df['Specialised Drama School'] = contains_keyword(actor_df['University'], 'drama')
    actor_df['Specialised Acting School'] = contains_keyword(actor_df['University'], 'acting')
    actor_df['Specialised Dance School'] = contains_keyword(actor_df['University'], 'dance')
    actor_df['Specialised Arts School'] = contains_keyword(actor_df['University'], 'arts')

    # Clean up column name (Admittedly a vestige but I cannot be bothered to change the name everywhere...)
    actor_df.rename(columns={'uni_rank': 'University Rank'})

    return