import pandas as pd
import numpy as np

def multiplier_generator(group, mul_factor=0.15, penalty_threshold=-0.25):
    """
    Calculates a cumulative score for an actor based on the 'Movie Success Index' 
    of their movies, applying a multiplier to each movie's score and penalizing 
    score drops below a threshold.

    Args:
        group (pd.DataFrame): Movie data for an actor, including 'Movie Success Index'.
        mul_factor (float): Multiplier factor for movie success index. Default is 0.15.
        penalty_threshold (float): Threshold for penalty based on score difference. Default is -0.25.

    Returns:
        pd.Series: The actor's 'Cumulative Score' based on their movies' success indices.
    """
    cumulative_log_multiplier = 0
    multiplied_scores = []
    prev_score = None

    for _, row in group.iterrows():
        if row['Movie star'] == group.name:
            score = 1.25 * row['Movie Success Index']
        else:
            score = row['Movie Success Index']

        #Define the multiplier proportional to the movie score
        multiplier = 1 + (score / 10) * mul_factor

        if prev_score is not None:
            score_diff_pct = (score - prev_score) / prev_score
            if score_diff_pct < penalty_threshold:
                multiplier *= 1 + score_diff_pct

        cumulative_log_multiplier += np.log(multiplier)
        cumulative_multiplier = np.exp(cumulative_log_multiplier)
        multiplied_scores.append(score * cumulative_multiplier)
        prev_score = score

    cumulative_score = np.log(sum(multiplied_scores) / len(multiplied_scores))
    return pd.Series({'Cumulative Score': cumulative_score})

def actor_success_index(character_movie_df):
    """
    Calculates the cumulative success score for each actor based on their movies' 
    'Movie Success Index', sorted by actor and release date.

    Args:
        character_movie_df (pd.DataFrame): DataFrame with movie and actor data.

    Returns:
        pd.DataFrame: DataFrame of actors with their cumulative success scores, sorted by score.
    """
    character_movie_df.sort_values(by=['Actor name', 'Movie release date_x'], inplace=True)

    actor_data = character_movie_df.groupby('Actor name').first().reset_index()
    cumulative_scores = character_movie_df.groupby('Actor name').apply(multiplier_generator).reset_index(drop=True)

    actor_data['Cumulative Score'] = cumulative_scores['Cumulative Score']
    
    actor_data.sort_values('Cumulative Score', ascending=False, inplace=True)
    actor_data['Actor Score Index'] = 10 * (
        actor_data['Cumulative Score'] - actor_data['Cumulative Score'].min()) / (
        actor_data['Cumulative Score'].max() - actor_data['Cumulative Score'].min())
    
    actor_data.set_index('Actor name', inplace=True)
    
    return keep_relevant_columns(actor_data)

def keep_relevant_columns(actor_data):
    columns_to_keep = [
        'Actor date of birth', 
        'Actor gender', 
        'Actor height',
        'Actor ethnicity',
        'Actor age at movie release',
        'Actor Score Index'
    ]
    actor_data = actor_data.loc[:, columns_to_keep]
    return actor_data

