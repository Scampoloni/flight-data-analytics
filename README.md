# Flight Data Analytics

A university data analytics project that collects real-time flight data via the OpenSky Network API, stores it in a MySQL database, and performs comprehensive data analysis including exploratory analysis, statistical testing, regression modeling, and unsupervised clustering.

---

## Research Question

> **Can flight velocity, altitude, and geographic position be used to predict and segment flight prices?**

---

## Data Source

**[OpenSky Network API](https://opensky-network.org/apidoc/)** — a free, open-source air traffic surveillance network that provides real-time and historical ADS-B flight state vectors (position, speed, altitude, heading, etc.) for civil aircraft worldwide.

---

## Project Workflow

```
OpenSky API
    │
    ▼
1. Data Collection          — Live API call → raw JSON stored to data/raw/
    │
    ▼
2. Data Cleaning &          — Filter airborne flights, drop nulls,
   Feature Engineering        engineer synthetic price variable
    │
    ▼
3. MySQL Storage            — Push cleaned DataFrame to a local MySQL database
    │                         via SQLAlchemy; aggregate queries with SQL
    ▼
4. Exploratory Data         — Descriptive statistics, histograms, scatter plots,
   Analysis (EDA)             boxplots, geographic map of flights
    │
    ▼
5. Statistical Analysis     — Pearson correlation (velocity ↔ price),
                              one-way ANOVA (price across top-5 countries)
    │
    ▼
6. Regression Modeling      — Linear Regression to predict price from
                              velocity, altitude, latitude, longitude;
                              evaluated with R² and RMSE
    │
    ▼
7. k-Means Clustering       — Segment flights into 3 groups by velocity,
                              altitude, and price using StandardScaler + KMeans
```

---

## Repository Structure

```
flight-data-analytics/
├── data/
│   ├── raw/
│   │   └── opensky_states_raw.json   # Original API response (JSON)
│   └── processed/
│       └── flights_clean.csv         # Cleaned & feature-engineered dataset
├── notebooks/
│   ├── Data_Analytics_Project.ipynb  # Main analysis notebook
│   └── Project_group_35.ipynb        # Group presentation notebook
├── presentation/
│   └── Project_Group_35.html         # Exported HTML presentation
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Dataset Description

The dataset is derived from a live snapshot of the **OpenSky Network** state vectors endpoint (`/api/states/all`). Each row represents one airborne aircraft at the time of the API call.

| Column           | Type    | Description                              |
|------------------|---------|------------------------------------------|
| `icao24`         | string  | Unique ICAO 24-bit aircraft address      |
| `callsign`       | string  | Aircraft callsign                        |
| `origin_country` | string  | Country of aircraft registration         |
| `latitude`       | float   | WGS-84 latitude in decimal degrees       |
| `longitude`      | float   | WGS-84 longitude in decimal degrees      |
| `velocity`       | float   | Ground speed in m/s                      |
| `geo_altitude`   | float   | Geometric altitude in meters             |
| `price`          | float   | **Synthetic** price variable (engineered)|

> **Note:** The `price` column is synthetically generated for educational purposes using a linear model of velocity and altitude plus random noise. It does not represent real ticket prices.

---

## Main Notebook

**[`notebooks/Data_Analytics_Project.ipynb`](notebooks/Data_Analytics_Project.ipynb)**

The notebook is structured into 7 sections mirroring the workflow above:

| Section | Description |
|---------|-------------|
| **1. Data Collection** | Fetches live data from the OpenSky REST API and saves raw JSON |
| **2. Data Preparation** | Cleans data, removes grounded aircraft, engineers the `price` feature |
| **3. Data Storage** | Writes data to MySQL via SQLAlchemy; executes aggregate SQL queries |
| **4. EDA** | Histograms, scatter plots, boxplots, and a geographic scatter map |
| **5. Statistical Analysis** | Pearson correlation test and one-way ANOVA |
| **6. Regression Modeling** | Train/test split, Linear Regression, R² / RMSE evaluation |
| **7. Clustering** | StandardScaler + KMeans (k=3), cluster profile summary |

---

## How to Run the Notebook

### Prerequisites

- Python 3.9+
- A running **MySQL** instance with a database named `flights_db`
  - Default connection string: `mysql+pymysql://root:passwort@localhost:3306/flights_db`
  - Update the connection string in **Section 3** of the notebook if needed

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Scampoloni/flight-data-analytics.git
cd flight-data-analytics

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter notebook notebooks/Data_Analytics_Project.ipynb
```

> If you do not have a MySQL server available, you can skip Section 3 (Data Storage) — all downstream analysis uses the in-memory `df_clean` DataFrame, not the database.

---

## Python Libraries Used

| Library | Purpose |
|---------|---------|
| `pandas` | Data manipulation and analysis |
| `numpy` | Numerical computing |
| `matplotlib` | Static plotting |
| `seaborn` | Statistical visualizations |
| `scikit-learn` | Machine learning (LinearRegression, KMeans, StandardScaler) |
| `scipy` | Statistical tests (Pearson correlation, ANOVA) |
| `requests` | HTTP calls to the OpenSky API |
| `sqlalchemy` | Database ORM / engine for MySQL |
| `pymysql` | MySQL driver (used by SQLAlchemy) |
| `jupyter` | Interactive notebook environment |

---

## Authors

**Group 35** — University Data Analytics Project
