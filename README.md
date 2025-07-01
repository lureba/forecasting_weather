# Vale do Paraíba Weather Forecasting

This project is an end-to-end data engineering and machine learning pipeline designed to collect, process, and forecast weather conditions for ten cities in the Vale do Paraíba region of São Paulo, Brazil. The entire workflow is orchestrated using Apache Airflow.

---

## Project Overview

The pipeline automates several key processes:

### Data Ingestion
Collects current weather data and geographic coordinates for specified cities using the OpenWeatherMap API.

### Web Scraping & NLP
Scrapes local news articles related to weather from 012news.com.br, then uses Google's Gemini API to perform Natural Language Processing (NLP), classifying the sentiment of each article in relation to temperature changes (e.g., significant increase, slight decrease).

### Database Management
Establishes a PostgreSQL database (`weather_vale`) and creates the necessary tables (`coordinates`, `scrapping`, `weather_`) to store the collected data.

### Data Orchestration
Utilizes Apache Airflow, configured via `docker-compose.yaml`, to manage and schedule the entire ETL (Extract, Transform, Load) workflow.

### Machine Learning Forecasting
Implements a time series forecasting model using skforecast and XGBoost to predict future minimum, maximum, and average temperatures. The process includes:

- **Feature Engineering**: Merging API data with scraped news classifications and creating categorical features.
- **Hyperparameter Tuning**: Using `grid_search_forecaster` to find the optimal parameters (`lags`, `n_estimators`, `max_depth`, etc.) for the XGBoost model.
- **Forecasting**: Training final models with the best parameters to predict future temperatures for the city of São José dos Campos.

---

## Core Components

### Data Sources
- **OpenWeatherMap API**: For raw weather metrics (temperature, humidity, pressure).
- **012 News**: For local news articles used as exogenous variables.

### Key Technologies
- **Orchestration**: Apache Airflow (with LocalExecutor)
- **Database**: PostgreSQL
- **Machine Learning**: Scikit-learn, Skforecast, XGBoost
- **NLP**: Google Gemini API
- **Containerization**: Docker (via `docker-compose`)

---

## Orchestration Environment

The `docker-compose.yaml` file sets up the Airflow environment, including the webserver, scheduler, triggerer, and a PostgreSQL backend for both Airflow's metadata and the project's data storage. Environment variables are used to manage credentials and API keys.

---

## Structure

The project is structured into several scripts and components:

### Database Initialization Scripts
A series of Python scripts create the PostgreSQL database and the required tables.

### Data Ingestion DAGs
- A DAG for fetching and storing city coordinates.
- A DAG for fetching and storing daily weather data from the API.

### Web Scraping DAG
A DAG that finds and scrapes relevant news URLs, processes the text with the Gemini API to generate a weather category, and stores the results in the database.

### Machine Learning Notebook/Script

- **Data Retrieval**: Connects to the PostgreSQL database to pull the weather and scraped data.
- **Feature Engineering**: Joins the datasets, handles missing values, and creates dummy variables from the text-based weather categories.
- **Model Training**: For each target variable (`temp_min`, `temp_max`, `actual_temp`):
  - Performs hyperparameter tuning using `grid_search_forecaster` and time series cross-validation (`TimeSeriesFold`).
  - Trains a final `ForecasterRecursive` model using the best found parameters.
- **Prediction & Evaluation**: Makes future predictions and provides functionality to inverse-transform the scaled predictions back to the original temperature scale.
