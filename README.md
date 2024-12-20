
# Beyond the spotlight: analysing key drivers of actors' long-term career success

> Applied Data Analysis - CS-401

* [Authors](#authors)
* [Abstract](#abstract)
* [Summary of P2](#summary-of-p2)
* [Research Questions](#research-questions)
* [Methods](#methods)
* [Organization within the Team](#organization-within-the-team)
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

### Discover the secrets of success—dive into the details on our official [site](https://elboyer228.github.io/sigma_squad_site/)

## Summary of P2

In our previous project milestone (P2), we focused on defining what success means for both actors and movies, embarking on the journey of creating a comprehensive success index for each. To achieve this, we identified the need for additional data and incorporated two new datasets to gain deeper insights into factors influencing success. Following this, we conducted data assessment and established selection criteria to determine which features were most relevant to success. This was followed by extensive data processing, transforming raw data into meaningful metrics aligned with our research goals. Detailed information about the datasets, preprocessing steps, and the development of the success index, along with our findings, can be found in the *Data Enrichment and Preprocessing* and *Success Index* sections of our project [site](https://elboyer228.github.io/sigma_squad_site/).

## Research Questions

* What additional attributes (e.g., education, theater background, sports involvement) could improve the regression model’s predictive power?

* How does an actor’s personal and professional background influence their career success?

## Methods

In this third milestone of the project, we encountered challenges due to extensive missing or non-interpretable data (e.g., ethnicity represented as codes like `/m/0bgcj46`) in the primary CMU Movie Summary Corpus.

Our goal was to create a meaningful final dataset with minimal missing values while retaining a sufficient number of actors to ensure a robust and coherent analysis. The steps and justifications for data reduction, as well as evidence that this reduction did not compromise our primary objective of analyzing key features influencing actor success, can be found in the [*results.ipynb* notebook](results.ipynb).

After cleaning the dataset, we supplemented it with additional data by scraping meaningful attributes such as university attended, theater involvement, sports participation, birth city, and number of children. This was done to explore whether seemingly unrelated features might play a role in determining an actor's success. The scraped data underwent further cleaning and analysis, resulting in the creation of a comprehensive final dataset.

Using this enriched and cleaned dataset, we analyzed the correlations between various features and actor success, gaining valuable insights into the factors that influence an actor’s career trajectory.

## Organization within the team

1. **Mael and Aiden**: **Web Scraping and Data Enrichment**

    * Collect additional data for actors, such as university attended, theater involvement, sports participation, birth city, and number of children.
    * Process and clean the scraped data to integrate it into the main dataset.
    * Ensure the quality and reliability of the enriched dataset.

2. **Pol**: **Correlation Analysis and Key Insights**

    * Perform correlation analysis between actor features and the success index.
    * Generate statistical insights into the relationships between variables.
    * Document the results and provide interpretations of the key correlations.

3. **Elise and Mathieu**: **Site Deployment and Data Storytelling**

    * Use Jekyll to set up and deploy the data story site on GitHub Pages.
    * Craft compelling narratives supported by visualizations and key findings.
    * Ensure a user-friendly and visually appealing presentation of the project’s results.

4. **Everyone**: **Visualization and Final Deliverables**

    * Create visualizations, such as correlation heatmaps, feature importance plots, and success prediction graphs.
    * Integrate the visuals into the data story to support the project’s narrative.
    * Finalize the Jupyter notebook with comprehensive documentation and ensure deliverables are polished for presentation.

## Project Structure

```
├── data                        <- Project datasets
│   └── ...
│
├── docs                        <- Documentation files
│   └── ...
│
├── plots_site                  <- Directory for plot outputs
│   └── ...
│
├── src                         <- Source code
│   ├── data                    <- Data processing scripts
│   │   ├── actor_data_completion.py        <- Functions for completing actor data
│   │   ├── correlation.py                  <- Functions for correlation analysis
│   │   ├── data_loader.py                  <- Functions for loading data
│   │   └──  transform_data.py              <- Functions for transforming data
│   │
│   ├── engines                 <- Engines for various tasks
│   │   ├── ethnicity_label_converting.py   <- Functions for converting ethnicity labels
│   │   ├── university_matching.py          <- Functions for matching universities
│   │   └── webscraping.py                  <- Functions for web scraping
│   │
│   ├── models                  <- Modeling scripts
│   │   ├── actor_success_model.py          <- Script for actor success index model
│   │   ├── linear_regression.py            <- Script regression analysis
│   │   └──  movie_success_model.py         <- Script for movie success index model
│   │
│   ├── utils                   <- Utility functions
│   │   └──  plot_graphs.py                 <- Functions for generating visualizations
│   │
│   └── constants.py            <- File containing constants
│
│
├── results.ipynb               <- Notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing Python dependencies
└── README.md                   <- Project overview and details
```

## Acknowledgements

We would like to thank our professor and teaching assistants for their guidance and support throughout this first part of our project. 😊
