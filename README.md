# OpenSky Flight Data Pipeline & Traffic Analytics

## Project Summary

University group project demonstrating an end-to-end analytics workflow using live OpenSky flight data, including API ingestion, JSON processing, data cleaning, MySQL storage, SQL analysis, exploratory data analysis, statistical testing, regression mechanics, and flight-profile clustering.

This is an educational project based on OpenSky ADS-B state-vector data. The `price` variable is synthetic: it does **not** represent real airline ticket prices. The regression section demonstrates methodology, not a real-world pricing model.

## Academic Context

The project was completed as a ZHAW university group assignment. Its value is the complete introductory workflow—from collecting a live API response to preparing data, querying it with SQL, and applying statistical and machine-learning methods—not a production aviation system.

## Research Question

> **How can live OpenSky flight-state data be collected, validated, stored, analysed, and segmented into interpretable flight profiles?**

Supporting questions:

- What altitude, velocity, and geographic patterns appear in the collected snapshot?
- How are observed aircraft distributed by country of registration?
- Can the observations be grouped into descriptive profiles with clustering?

The resulting clusters are exploratory groupings, not official aircraft or flight categories.

## Data Source

The data comes from the [OpenSky Network REST API](https://openskynetwork.github.io/opensky-api/rest.html), specifically the `/api/states/all` endpoint. Its state vectors describe observed aircraft states such as position, velocity, altitude, heading, and country of registration. They do not contain fares, routes, origins, destinations, or ticket prices.

The committed raw JSON and processed CSV preserve an example snapshot, so the analysis can be inspected without making a new API request.

## End-to-End Workflow

```mermaid
flowchart LR
    A["OpenSky API"] --> B["Raw JSON"]
    B --> C["Cleaning and feature preparation"]
    C --> D["MySQL"]
    D --> E["SQL / EDA / statistics"]
    E --> F["Regression demonstration and clustering"]
```

The notebooks:

1. request a live state-vector snapshot and store the raw JSON;
2. retain airborne observations, require coordinates, trim callsigns, and create the educational synthetic variable;
3. optionally write selected fields to MySQL through SQLAlchemy and run an aggregate SQL query;
4. perform descriptive and visual exploration;
5. run Pearson correlation and one-way ANOVA exercises;
6. demonstrate a train/test regression workflow; and
7. standardise selected variables and apply KMeans clustering.

## Dataset Description

Each processed row represents one airborne aircraft observation from a live snapshot.

| Column | Meaning |
|---|---|
| `icao24` | ICAO 24-bit aircraft address |
| `callsign` | Broadcast callsign, when available |
| `origin_country` | Country of aircraft registration; not flight origin |
| `latitude`, `longitude` | WGS-84 coordinates in decimal degrees |
| `velocity` | Ground speed in metres per second |
| `baro_altitude`, `geo_altitude` | Barometric and geometric altitude in metres |
| `on_ground` | OpenSky ground-status flag |
| `price` | Synthetic educational variable generated from velocity, geometric altitude, and random noise |

The remaining fields are preserved from the OpenSky state-vector schema. See the notebooks for the complete column list.

## SQL and Database Integration

The database section uses SQLAlchemy with the PyMySQL driver to write a `flights` table to MySQL. It then runs a grouped SQL query by `origin_country`, including counts and aggregates of the synthetic variable.

Connection details are read from `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD`; credentials are not stored in the notebooks. The MySQL cells are optional and can be skipped together. Later EDA, statistics, regression, and clustering cells continue from the in-memory `df_clean` DataFrame.

## Exploratory and Statistical Analysis

The notebooks include descriptive statistics, histograms, scatter plots, boxplots, and a coordinate scatter plot. Pearson correlation examines velocity against the synthetic `price`; one-way ANOVA compares that synthetic variable across the five most frequent registration countries in the snapshot.

These tests demonstrate statistical mechanics on the educational dataset. They do not establish airline pricing relationships or causal aviation findings.

## Flight-Profile Clustering

KMeans with `k=3` is applied after standardising velocity, geometric altitude, and the synthetic variable. The resulting groups are useful for practising preprocessing and cluster profiling, but they are descriptive only. Because one clustering feature is synthetic, the clusters must not be interpreted as real fare segments, official operational categories, or aircraft classes.

## Educational Regression Demonstration

The academic submission retains a linear-regression exercise using velocity, geometric altitude, latitude, and longitude to estimate the synthetic `price` target. The target was constructed partly from velocity and geometric altitude, so predictors used by the regression also contributed to target generation.

Consequently, the reported model performance is **not** evidence that flight-state data can predict real ticket prices. The section demonstrates train/test splitting, fitting a linear regression, generating predictions, and calculating RMSE and R².

## Repository Structure

```text
flight-data-analytics/
├── data/
│   ├── raw/opensky_states_raw.json
│   └── processed/flights_clean.csv
├── notebooks/
│   ├── Data_Analytics_Project.ipynb
│   └── Project_group_35.ipynb
├── presentation/Project_Group_35.html
├── scripts/validate_data.py
├── .env.example
├── README.md
└── requirements.txt
```

[`notebooks/Data_Analytics_Project.ipynb`](notebooks/Data_Analytics_Project.ipynb) is the main analysis notebook. [`notebooks/Project_group_35.ipynb`](notebooks/Project_group_35.ipynb) and the [HTML export](presentation/Project_Group_35.html) retain the group-presentation version of the academic work.

## Local Setup

Python 3.12 is recommended because the notebook metadata records Python 3.12.7.

```bash
git clone https://github.com/Scampoloni/flight-data-analytics.git
cd flight-data-analytics
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and launch the main notebook:

```bash
python -m pip install -r requirements.txt
jupyter notebook notebooks/Data_Analytics_Project.ipynb
```

Before running the optional MySQL section, create a database, use `.env.example` as a reference, and set the five variables in the shell that launches Jupyter. For example:

```powershell
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "flights_db"
$env:MYSQL_USER = "your_mysql_user"
$env:MYSQL_PASSWORD = "your_mysql_password"
jupyter notebook notebooks/Data_Analytics_Project.ipynb
```

The notebook does not automatically load `.env` files. If MySQL is unavailable, skip all cells in Section 3; subsequent analysis uses `df_clean` rather than the SQL result.

To validate the committed processed CSV without calling the API or MySQL:

```bash
python scripts/validate_data.py
```

## Project Context and Contribution

This was a ZHAW university group project.

**Individual contribution: TODO — add the specific parts personally implemented or analysed.**

The available repository history does not provide enough evidence to attribute particular notebook sections to one person, so no individual contribution claim is made here.

## Limitations

- The files may represent only a single live snapshot; traffic changes by time, coverage, and API availability.
- `origin_country` is the country of aircraft registration, not the flight's origin or destination.
- ADS-B state vectors do not include ticket prices; `price` is synthetic and educational.
- Missing coordinates, callsigns, altitude, and other state-vector values are common.
- Live OpenSky availability, response size, authentication requirements, and rate limits may vary.
- Snapshot patterns should not be generalised to the global aviation system.
- Pearson correlation and ANOVA involving `price` describe a constructed variable, not market pricing.
- Regression performance is influenced by target construction and has no real pricing validity.
- KMeans output is descriptive, sensitive to selected features and `k`, and is not an official classification.
- No operational, causal, or aviation-safety conclusions should be drawn.

## Authors / Group Context

**Group 35 — ZHAW University Data Analytics Project**

The repository preserves the original group notebooks and presentation. Add the verified names and roles of all group members here if the group has agreed to publish them.
