# Movie Data Pipeline (ETL Assignment)

##  Overview
This project implements a simple data pipeline using MovieLens CSV files and the OMDb API.
It extracts, transforms, enriches, and loads movie data into an SQLite database.

The pipeline:
- Extracts movies & ratings from MovieLens
- Cleans and transforms the dataset
- Enriches movies using the OMDb API
- Loads everything into SQLite using a defined schema
- Runs analytical SQL queries

---

##  Project Structure

movie-data-pipeline/
├── etl.py
├── schema.sql
├── queries.sql
├── README.md
└── data/
├── movies.csv
└── ratings.csv


---

##  Setup Instructions

### 1. Create Virtual Environment


python -m venv venv


### 2. Activate (Windows PowerShell)


.\venv\Scripts\Activate.ps1


### 3. Install Requirements


pip install pandas requests python-dotenv


### 4. Create `.env` file
Create a file named `.env` in the project folder and add:


OMDB_API_KEY=your_api_key_here


### 5. Add Dataset
Download MovieLens “latest-small” from Grouplens and place:


movies.csv
ratings.csv

inside the `data/` folder.

---

##  Running the ETL Pipeline


python etl.py

Expected output:


 ETL Completed Successfully!
 movies.db is ready.


---

##  Running SQL Queries
Use DB Browser for SQLite:
1. Open `movies.db`
2. Go to **Execute SQL**
3. Copy & paste queries from `queries.sql`
4. Run and view results

---

##  Design Choices
- SQLite chosen to avoid setting up a database server
- Enriched only the first 15 movies to avoid free OMDb API limits
- Added title cleaning and fallback search to improve OMDb matching
- Schema kept simple and easy to understand for learning purposes

---

##  Challenges Faced
- Some MovieLens titles did not match OMDb format → solved using title cleanup + multiple search attempts  
- PowerShell blocked virtual environment activation → fixed using execution policy bypass  
- `.env` didn’t load at first because of incorrect file placement → fixed by placing it next to `etl.py`  

---

 **Project complete and ready for review.**
