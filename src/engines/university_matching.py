import pandas as pd
from src.constants import EXCEPTIONS_LIST
from rapidfuzz import process


class UniversityMatchEngine:
    '''
    Class used to match university names to a list of known university names using fuzzy matching,
    '''
    def __init__(self):
        self.rankings_df = self.load_rankings()
        self.qs_uni_names_list = self.rankings_df['Institution Name'].to_list()
        self.rankings_dict = self.create_rankings_dict()
        self.list_of_exceptions = EXCEPTIONS_LIST
        pass

    def load_rankings(self):
        """
        Loads the QS World University Rankings data.
        """
        return pd.read_csv('data/2024_QS_World_University_Rankings.csv')

    def create_rankings_dict(self):
        """
        Create a dictionary with university names as keys and their rankings as values.
        """
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
        """
        Check if a given keyword is present in the given column.

        Args:
            column (pd.Series): The column to search within.
            keyword (str): The keyword to search for in the column.

        Returns:
            pd.Series: A Series of integers where 1 indicates the presence of the keyword and 0 indicates its absence.
        """
        return column.str.contains(keyword, case=False, na=False).astype(int)

    def replace_exceptions(self, actor_df: pd.DataFrame):
        """
        Replaces specific exceptions in the 'University' column of actor_df DataFrame.
        """

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
        """
        Attempts to match universities in the given actor_df DataFrame with a predefined list of universities.
        """

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
        """
        Converts a university ranking string to an int.

        Args:
            rank (str): The ranking string to be cleaned.

        Returns:
            int or str: The cleaned ranking as an int, or 'Not Ranked' if the input is 'Not Ranked'.
        """
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
        """
        Adds QS University Rank to the actor DataFrame based on the university name.
        """
        actor_df['QS University Rank'] = actor_df['University'].map(self.rankings_dict)
        actor_df['QS University Rank'] = actor_df['QS University Rank'].fillna('Not Ranked')
        actor_df['QS University Rank'] = actor_df['QS University Rank'].apply(self.clean_rank)
        return

    def clean_universities(self, actor_df: pd.DataFrame):
        """
        Cleans and processes the 'University' column in the actor_df DataFrame.
        Adds university rank information.
        Creates binary columns indicating if the actor attended a specialised school.
        """

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
