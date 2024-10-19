# Tennis Analysis and Gambling

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Project Overview

The goal of this project is to analyze betting odds from past ATP and WTA tennis matches. By leveraging historical data, the project aims to uncover patterns and insights that can enhance betting strategies.

## Data Sources

All datasets are sourced from [Tennis Data](http://www.tennis-data.co.uk/alldata.php). This repository provides comprehensive historical match data for both ATP and WTA events.

### Data Acknowledgements

For information on the data files and sources, please refer to the text file key: [Data File Key](http://www.tennis-data.co.uk/notes.txt).

## Features

- **Data Collection**: Functions to download and save historical match data for ATP and WTA from the provided source.
- **Data Cleaning**: Utilities to clean and preprocess match data, ensuring consistency and readiness for analysis.
- **Elo Rating System**: Implementation of the Elo ranking system to evaluate player performance based on match outcomes.
- **Feature Engineering**: Creation of new features from match data, including odds and rankings, to facilitate deeper analysis.
- **Analysis & Insights**: Tools for analyzing betting odds and predicting match outcomes based on historical data.

## Installation

To get started, clone the repository and install the necessary dependencies:

```bash
git clone <repository_url>
cd tennis_analysis_and_gambling
pip install -r requirements.txt
