
# Beyond the spotlight: analysing key drivers of actors' long-term career success

> Applied Data Analysis - CS-401

## Contents

* [Authors](#authors)
* [Abstract](#abstract)
* [Research Questions](#research-questions)
* [Additional Datasets](#additional-datasets)
* [Methods](#methods)
* [Timeline](#timeline)
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

1. **Movie Success Index**:
   We will construct a weighted index for movie success using factors such as IMDb rating, review count, number of nominations, revenue, budget and genre. Each factor will be scaled from 0 to 10, with the weights summing to 1.

2. **Actor Success Analysis**:
    Based on the movies identified as successful, we will trace the actors involved and calculate each actor's "success index" based on the average success scores of their films.

3. **Predictive Analysis**:
    Using regression models, we will analyse the correlation of various actor attributes with their career success.

## Project P2 timeline

The project will span two weeks, from November 4th to November 15th. Our weekly goals are as follows:

* First week (Nov 4th to 10th): redefine the project’s problem statement and key questions, assess the project’s feasibility with the available data, and explore additional datasets for inclusion.
* Second week (Nov 11th to 15th): develop the success index by identifying key factors and determining the appropriate weighting for accurate results.

## Organization within the team

## Questions for TAs

* How do we handle missing data effectively when calculating the success index?

## Project Structure

The directory structure of new project looks like this:

```
├── data                        <- Project data files
│   ├── character.metadata.tsv          <- Metadata for characters
│   ├── movie_data_tmbd.csv             <- Movie data from TMDB
│   ├── movie.metadata.tsv              <- Metadata for movies
│   ├── scrithe_oscar_awardpts.csv      <- Data on Oscar awards
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```

## Acknowledgements

We would like to thank our professor and teaching assistants for their guidance and support throughout this first part of our project. 😊
