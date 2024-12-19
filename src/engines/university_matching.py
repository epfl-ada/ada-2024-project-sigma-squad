import pandas as pd
from rapidfuzz import process


class UniversityMatchEngine:

    def __init__(self):
        self.rankings_df = pd.read_csv('data/2024_QS_World_University_Rankings.csv')
        self.qs_uni_names_list = self.rankings_df['Institution Name'].to_list()
        self.rankings_dict = self.create_rankings_dict()
        self.list_of_exceptions = [
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
        pass


    def create_rankings_dict(self):
        # Create a dictionary with university name as key and ranking as value
        return self.rankings_df.set_index('Institution Name')['2024 QS World University Rankings'].to_dict()


    def match_universities(self, uni_name):
        """
        Matches the university name to the list of university names using fuzzy matching,
        if the confidence is below 88.

        Args:
            uni_name: The name of the university to match.
        """
        
        if not isinstance(uni_name, str):  # Check if the value is NaN
            return None
        result = process.extractOne(uni_name, self.qs_uni_names_list)
        if result:
            match, score, _ = result  # Unpack match, score, and index
            return match if score > 88 else None  # Return match only if confidence > 88
        return None
    

    def contains_keyword(self, column, keyword):
        return column.str.contains(keyword, case=False, na=False).astype(int)
    

    def replace_exceptions(self, actor_df: pd.DataFrame):

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

        for (word, school) in self.list_of_exceptions:
            actor_df.loc[
                actor_df['University'].str.contains(word, case=False, na=False),
                'University'
            ] = school

        return
    

    def try_matching(self, actor_df: pd.DataFrame):

        actor_df['Matched Uni'] = actor_df['University'].apply(self.match_universities)
        
        # Replace the original values of the university with those found through matching, allows to attach rank from QS
        actor_df['University'] = actor_df.apply(
            lambda row: row['Matched Uni'] if pd.notna(row['Matched Uni']) else row['University'], axis = 1
        )

        # Create binary indicator of whether or not a match was found
        actor_df['found_match'] = actor_df.apply(lambda row: True if pd.notna(row['Matched Uni']) else False, axis=1)

        # Remove the now unnecessary column
        actor_df.drop(columns=['Matched Uni'], inplace=True)

        return
    

    def clean_rank(self, rank):
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
        

    def add_university_rank(self, actor_df):
        actor_df['QS University Rank'] = actor_df['University'].map(self.rankings_dict)
        actor_df['QS University Rank'] = actor_df['QS University Rank'].fillna('Not Ranked')
        actor_df['QS University Rank'] = actor_df['QS University Rank'].apply(self.clean_rank)
        return


    def clean_universities(self, actor_df: pd.DataFrame):

        # First round of matching the institution names to the universities
        self.try_matching(actor_df)

        # Replace useless values with None and replace exceptions
        self.replace_exceptions(actor_df)

        # Second round of matching the institution names to the universities
        self.try_matching(actor_df)

        # Specify those that did not go to uni
        actor_df['University'] = actor_df['University'].fillna('Did not go')

        # Replace Schools that are not in the QS list with 'sub 1500 school'
        actor_df.loc[
            (actor_df['found_match'] == False) &  # Check if 'found_match' is False
            (~(actor_df['University'] == 'Did not go')) & # Check if empty
            (~actor_df['University'].str.lower().str.startswith('specialised', na=False)) &  # Does NOT start with 'specialised'
            (~actor_df['University'].str.lower().str.startswith('vassar', na=False)),  # Does NOT start with 'vassar'
            'University'
        ] = 'sub 1500 school'

        actor_df.drop(columns=['found_match'], inplace=True)

        self.add_university_rank(actor_df)

        # Create a binary column: 1 if 'uni_rank' is numeric, 0 if 'Not Ranked'
        actor_df['Ranked Uni'] = actor_df['QS University Rank'].apply(lambda x: 1 if isinstance(x, int) else 0)

        # Replace 'Not Ranked' with a placeholder of 3000 (very large)
        actor_df['Usable Uni Rank'] = actor_df['QS University Rank'].apply(lambda x: x if isinstance(x, int) else 3000)

        # Create binary columns of whether or not the actor went to a specialised school
        actor_df['Specialised Drama School'] = self.contains_keyword(actor_df['University'], 'drama')
        actor_df['Specialised Acting School'] = self.contains_keyword(actor_df['University'], 'acting')
        actor_df['Specialised Dance School'] = self.contains_keyword(actor_df['University'], 'dance')
        actor_df['Specialised Arts School'] = self.contains_keyword(actor_df['University'], 'arts')
        return
