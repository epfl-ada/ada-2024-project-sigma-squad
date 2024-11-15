
# Beyond the spotlight: analysing key drivers of actors' long-term career success

> Applied Data Analysis - CS-401

## Contents

* [Authors](#authors)
* [Abstract](#abstract)
* [Research Questions](#research-questions)
* [Additional Datasets](#additional-datasets)
* [Methods](#methods)
* [Roadmap](#roadmap)
* [Organization within the Team](#organization-within-the-team)
* [Questions for TAs](#questions-for-tas)
* [Project Structure](#project-structure)
* [Acknowledgements](#acknowledgements)

## Authors

* Élise Boyer ([@elboyer228](https://github.com/elboyer228))
* Pol Fuentes ([@SpaceMercury](https://github.com/SpaceMercury))
* Mathieu Sanchez ([@matsanch](https://github.com/matsanch))
* Mael Studer ([@maelstuder](https://github.com/maelstuder))
* Aiden Tschammer-Osten ([@Hoodie031](https://github.com/Hoodie031))

## Abstract

We aim to analyse the factors contributing to the long-term career success of actors in the film industry. We seek to explore what sets successful actors apart. Starting from a bottom-up approach, we will first establish a "success index" for movies based on various weighted factors, such as ratings, revenue, awards, and popularity. Once we identify the most successful movies, we will trace the actors involved and evaluate their career paths, identifying trends that may contribute to their success. We will then explore specific actor attributes—such as genre specialization, age at career start, and frequency of successful roles—to determine correlations and potential predictors of sustained success. Ultimately, our goal is to offer a data-driven understanding of what makes certain actors thrive in the competitive film industry.

## Research Questions

* How can we define and calculate a "success index" for movies, and what factors should it include?
* Does an actor’s age at career start, choice of genres, or frequency in high-grossing movies correlate with their career success?
* Can we use these findings to predict the likelihood of success for actors based on early-career indicators?

## Additional datasets

To enrich our analysis, we will use the following additional datasets:

* **The Oscar Award Dataset**  
  Source: [Kaggle - The Oscar Award](https://www.kaggle.com/datasets/unanimad/the-oscar-award)  
  This dataset provides information on Oscar nominations and wins. It includes details such as categories, winners, and nominees across multiple years. This will help us assess the impact of awards on career success.

* **TMDb Movie Dataset**  
  Source: [IMDb - Dataset](https://github.com/danielgrijalva/movie-stats)  
  This dataset contains information on 6,820 movies released from 1986 to 2016, including details on budget, production company, country, director, genre, gross revenue, name, rating, release date, runtime, IMDb score, user votes, main actor, writer, and release year.

Note on dataset choice: initially, we considered a larger dataset from [Kaggle - TMDb Data 09/20](https://www.kaggle.com/datasets/kakarlaramcharan/tmdb-data-0920), which contained approximately 119 000 movies with 27 features each. However, during preprocessing, we found significant data quality issues, particularly with key features like budget. For instance, some movies had a budget of "1," while others showed accurate values like "23 million," suggesting inconsistencies beyond simple unit errors; or, for some movies, a budget of "30" was listed where the actual budget was 30 million. Considering the unreliability of this dataset, we chose a smaller one that still includes the features of interest but with more accurate values, ensuring the reliability of our calculated index. Validation of these results is available in the results.ipynb notebook.

## Methods

1. **Data Assesment and Selection of Criteria**: To ensure a reliable success index, we focused on critcal factors such as **budget**, **revenue**, **ratings**, **Oscar nominations**, and **profitability**. After assessing the CMU Movie dataset and additional sources, we found that 3537 movies meet our criterias with sufficient data for analysis and creating a robust index.  

2. **Movie Success Index**: The movie success index adds four primary factors. probitability, revenue, reviews and Oscar nominations, each, scaled from 0 to 10 for comparability. The aspects of these factors are:

    * **Probitability**:
          Calculated as the ratio of revenue to budget, with a log transform to reduce the effect of outliers, then normalized.
    * **Revenue**:
          Scaled using a log10 to balance large and small revenue and giving a score from 0-10.
    * **Oscar Score**:
          Acts as a multiplier to reward movies with high acclaim, and having decayed returns for subsequent nominations.
    * **Reviews**:
          Taken as such, having already a score from 0-10.

      The final index is then weighted with 35% profitability and revenue, 30% reviews and is finally scaled from 0-10, giving us the final success index for the movies.

3. **Actor Success Analysis**: Based on the movies identified as successful, we will trace the actors involved and calculate each actor's "success index" based on the average success scores of their films. The index is based off a **multiplier** and **streak system** which values **consistency** and **frequency of success**. Additionally, actors that are the stars of their movie receive a bonus for that specific movie.

    * **Calculation of the multplier**:
    Successive movies by the same actors are given a multiplier based on wether they improve or decline upon from the previous movie's score. Improvements lead to greater multipliers while drops penalizes the score. This ensures that consistent actors are more rewarded.
    * **Cumulative Scoring**:
    Each movie index is adjusted by the cumulative multiplier, log10-transformed and normalized to gives us a consistent 0-10 metric to comparing actors' career trajectories.

4. **Predictive Analysis**:
    Using regression models, we will analyse the correlation of various actor attributes with their career success. This approach would involve using regression models to predict an actor’s success index based on features like genre diversity, frequency of high-scoring movies, age at career start, height, etc.

## Roadmap

1. **Week 1**: Create and finalize the regression model, choosing features like early career movie scores, genre diversity, frequency of high grossing roles or even more bold features like height, ethnicity and gender. Validate the results of the model.

2. **Week 2**: Develop and integrate visualizations (correlation heatmaps, feature importance plots) to illustrate our findings. Draft the data story from these findings. Create a 'Your actor career' app that predicts the career the user would have based on his inputs.

3. **Week 3**: Finalize the Jupyter notebook by cleaning up the code, documenting it compenduously. Host the data story with Jekyll and ensure the story is engaging and the app working.

## Organization within the team

1. **Mael**: **Feature Engineering and Data Preprocessing**

    Select and preprocess features for the regression model (e.g., early career scores, genre diversity, high-grossing roles, height, ethnicity, gender).
    Normalize and handle missing data and validate the dataset.

2. **Aiden**: **Regression Modeling and Validation**

    Develop the regression model using selected features.
    Tune hyperparameters and evaluate the model with training and testing datasets.
    Document the modeling process and summarize validation results.

3. **Mathieu**: **Visualization and Data Story Insights**

    Create visualizations, including correlation heatmaps, feature importance plots, and predictions vs. actuals graphs.
    Analyze visual insights to support the narrative of the data story. Draft the story’s key findings and flow.

4. **Pol**: **App Development and User Interaction**

    Develop the "Your Actor Career" app to predict user-defined career trajectories based on the regression model.
    Document the app’s workflow and features.

5. **Elise**: **Documentation and Final Deliverables**

    Finalize and clean up the Jupyter notebook, ensuring clear and comprehensive documentation.
    Set up Jekyll for hosting the data story on GitHub Pages.

## Questions for TAs

* Are there best practices for validating weights in a composite index like ours?

## Project Structure

```
├── data                        <- Project datasets
│
├── src                         <- Source code
│   ├── data                    <- Data processing scripts
│   │   ├── data_loader.py      <- Functions for loading data
│   │   ├── transform_data.py   <- Functions for transforming data
│   │
│   ├── models                  <- Modeling scripts
│   │   ├── actor_success_model.py  <- Script for actor success index model
│   │   ├── movie_success_model.py  <- Script for movie success index model
│   │
│   ├── utils                   <- Utility functions
│       ├── plot_graphs.py      <- Functions for generating visualizations
│
├── results.ipynb               <- Notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing Python dependencies
└── README.md                   <- Project overview and details
```

## Acknowledgements

We would like to thank our professor and teaching assistants for their guidance and support throughout this first part of our project. 😊
