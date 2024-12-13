import pandas as pd
import numpy as np

from src.data.transform_data import raw_data, clean_data


# Profitability factor:

def profitability_factor(df):
    """
    Calculates the profitability factor for each movie in the DataFrame.

    This function computes a 'Profitability' column as the ratio of movie 
    box office revenue to budget. It then applies a logarithmic transformation 
    to reduce the influence of outliers and normalizes the result on a 0-10 scale 
    to produce a 'Profitability Score'.

    Returns:
        None: Modifies the global DataFrame `df` in place by adding the column:
            - 'Profitability Score': Normalized score on a 0-10 scale.
    """

    df['Profitability'] = df['Movie box office revenue'] / df['Movie budget']

    # Apply log to diminish the influence of high values
    df['Log Profitability'] = df['Profitability'].apply(np.log)

    # Normalize the log values to a 0-10 scale
    df['Profitability score'] = 10 * (df['Log Profitability'] - df['Log Profitability'].min()) / (
                                           df['Log Profitability'].max() - df['Log Profitability'].min())
    return 


# Revenue factor:

def revenue_factor(df):
    """
    Calculates the revenue factor for each movie in the DataFrame.

    This function computes a 'Revenue Score' based on the logarithmic 
    transformation of the movie box office revenue. The score is normalized 
    on a 0-10 scale to provide a relative measure of each movie's revenue.

    Returns:
        None: Modifies the global DataFrame `df` in place by adding the column:
            - 'Revenue Score': Normalized revenue score on a 0-10 scale.
    """

    df['Log Revenue'] = np.log10(df['Movie box office revenue'] + 1)
    df['Revenue score'] = 10 * (df['Log Revenue'] - df['Log Revenue'].min())/(df['Log Revenue'].max() - df['Log Revenue'].min())
    return 


# Movie review factor:

def review_factor(df):
    """
    Placeholder for the movie review score.
    """
    return 


# Number of oscar nominations multiplication factor:

def oscar_mult_factor(df):
    """
    Calculates an Oscar-nomination-based multiplication factor for each movie.

    Returns:
        None: Modifies the global DataFrame `df` in place by adding the column:
            - 'Oscar Multiplication Factor': Adjusted score based on Oscar nominations.
    """

    multiplier_weight = 0.25/np.log(df['Number of nomination'].max()+1)

    # Score of 0 for movies with no nominations
    #df['Number of nomination'].fillna(0, inplace=True)
    df.fillna({'Number of nomination': 0}, inplace=True)
    df['Oscar Multiplication Factor'] = 1 + multiplier_weight * (np.log(df['Number of nomination'] +1))
    
    return 


# Success Index:

def movie_success_index(df):
    """
    Calculates the success index of each movie.

    This function combines the profitability factor, revenue factor, review 
    factor, and Oscar-based multiplication factor to produce a final 'Movie Success 
    Index'. Each component is weighted according to specified values. The resulting 
    success index provides a normalized score on a 0-10 scale, indicating overall 
    movie success.

    Returns:
        pd.DataFrame: The global DataFrame `df` with the following additional columns:
            - 'Movie Success Index': The final success index for each movie.
    """

    profitability_factor(df)
    revenue_factor(df)
    review_factor(df)
    oscar_mult_factor(df)

    # Chosen weights
    profitability_weight = 0.35
    revenue_weight = 0.35
    review_weight = 0.3

    max_possible_score = (
        10 * profitability_weight +
        10 * revenue_weight +
        10 * review_weight
    ) * df['Oscar Multiplication Factor'].max()

    # Success index calculation
    df['Movie Success Index'] = (
        (df['Profitability score'] * profitability_weight +
         df['Revenue score'] * revenue_weight +
         df['Review score'] * review_weight) *
         df['Oscar Multiplication Factor']
    ) / max_possible_score *10

    return 



if __name__ == "__main__":
    df = clean_data(raw_data())
    
    movie_success_index(df)

    print(df.sort_values(by='Profitability score', ascending = False))
    print()

    print(df.sort_values(by='Revenue score', ascending = False))
    print()

    print(df.sort_values(by='Review score', ascending = False))
    print()

    print(df.sort_values(by='Oscar Multiplication Factor', ascending = False))
    print()

    print(df.sort_values(by='Movie Success Index', ascending = False))
    print()
