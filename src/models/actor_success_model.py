import pandas as pd
import numpy as np

from src.data.transform_data import raw_data, clean_data, actor_data

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
    actor_mult_movies = character_movie_df.sort_values(by=['Actor name', 'Movie release date_x']).reset_index(drop=True)
    actor_scores = actor_mult_movies.groupby('Actor name').apply(multiplier_generator)
    actor_scores = actor_scores.sort_values('Cumulative Score', ascending=False)
    actor_scores['Actor Score Index'] = 10 * (
        actor_scores['Cumulative Score'] - actor_scores['Cumulative Score'].min()) / (
        actor_scores['Cumulative Score'].max() - actor_scores['Cumulative Score'].min())
    return actor_scores


if __name__ == "__main__":
    df = clean_data(raw_data())
    #movie_success_index(df)

    merged_character_movie_df = actor_data(df)
    actor_success = actor_success_index(merged_character_movie_df)
    print(actor_success.head())
