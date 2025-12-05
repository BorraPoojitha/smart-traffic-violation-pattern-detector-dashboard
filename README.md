# 🚦 Smart Traffic Violation Pattern Detector Dashboard v0.1.0

## 📝 Overview

This project is a Streamlit web application designed to analyze traffic violation data. It provides a user-friendly interface to explore, visualize, and gain insights from traffic violation datasets. Users can upload their own data, perform analysis, and view summaries and trends.

## ✨ Features

* **Dataset Management:**
  * Upload your own CSV datasets.
  * View and browse the loaded dataset.
* **Numerical Analysis:**
  * Get a quick overview of your dataset, including shape and sample rows.
  * View detailed information about each column, including data types and descriptive statistics.
* **Data Visualization:**
  * Generate various plots to visualize data distributions and relationships.
* **Trend Analysis:**
  * Analyze trends in the data over time.
* **Map Visualization:**
  * Visualize geographical data on an interactive map.
* **Correlation Analysis:**
  * Explore correlations between numerical columns with a heatmap.

## 🚀 How to Run

1. **Clone the repository:**

    ```bash
    git clone https://github.com/saidulalimallick04/smart-traffic-violation-pattern-detector-dashboard.git
    cd smart-traffic-violation-pattern-detector-dashboard
    ```

2. **Choose your package manager:**

    ---

   ### Alternative 1: Using `uv` (Recommended)

    1. **Create and activate a virtual environment:**

        ```bash
        # Create a virtual environment
        uv venv
        
        # Activate the virtual environment
        # On Windows
        .\.venv\Scripts\activate
        # On macOS/Linux
        source .venv/bin/activate
        ```

    2. **Install dependencies:**

        ```bash
        uv pip install .
        ```

    3. **Run the application:**

        ```bash
        streamlit run app.py
        ```

    ---

   ### Alternative 2: Using `pip`

    1. **Create and activate a virtual environment:**

        ```bash
        python -m venv .venv
        # On Windows
        .\.venv\Scripts\activate
        # On macOS/Linux
        source .venv/bin/activate
        ```

    2. **Install dependencies:**

        ```bash
        pip install .
        ```

    3. **Run the application:**

        ```bash
        streamlit run app.py
        ```

## 📂 Project Structure

```text
.
├── .gitignore
├── .python-version
├── app.py
├── core
│   ├── __init__.py
│   ├── analysis_plot.py
│   ├── dashboard_plot.py
│   ├── dashboard_summary.py
│   ├── data_generator.py
│   ├── data_variables.py
│   ├── sidebar.py
│   ├── trend_plot.py
│   ├── utils.py
│   └── visualization_plot.py
├── dataset
│   └── Indian_Traffic_Violations.csv
├── generated_fake_traffic_datasets
│   └── 2025-11-24
│       ├── 01_traffic_dataset.csv
│       └── 02_traffic_dataset.csv
├── map_data
│   ├── 01_INDIA_STATES.geojson
│   └── 02_INDIA_STATES.geojson
├── other_party_uploads
│   └── AnimalDataLabel.csv
├── pages
│   ├── 01_Numerical_Analysis.py
│   ├── 02_Visualize_Data.py
│   ├── 03_Trend_Analysis.py
│   ├── 04_Map_Visualization.py
│   ├── 09_Upload_Dataset.py
│   └── 10_View_Dataset.py
├── pyproject.toml
├── README.md
├── related_uploads
└── uv.lock
```

## 📦 Dependencies

The main dependencies for this project are listed in the `pyproject.toml` file. They include:

* `streamlit`
* `pandas`
* `numpy`
* `seaborn`
* `matplotlib`
* `plotly`
* `folium`
* `streamlit-folium`

## Recent Updates

* **2025-12-05:**
  * **Code Refactoring:** Refactored plotting logic into dedicated modules (`core/dashboard_plot.py`, `core/analysis_plot.py`, `core/trend_plot.py`, `core/visualization_plot.py`) to improve code organization and maintainability.
* **2025-11-24:**
  * **Fake Data Generation:** Enhanced the fake data generator to produce more varied and realistic datasets. The possibilities for randomly generated data have been increased by expanding the variable lists and mappings.
* **2025-11-22:**
  * **Dashboard Overhaul:** Revamped the main dashboard with a dynamic summary of the last N days, including:
    * Total violations and distribution by type.
    * Total fines generated, with a breakdown of paid vs. unpaid amounts.
    * Violations by location, visualized with a pie chart.
    * Key driver insights, including average age and gender distribution.
  * **Fake Data Generator:** Added a new feature to generate realistic fake traffic violation datasets for testing and demonstration.
  * **Improved Dataset Management:**
    * Enhanced the sidebar to organize datasets into categories: `Sample`, `Generated`, `Traffic Related`, and `Other`.
    * Updated file upload logic to automatically classify and store datasets based on their columns.
* **2025-11-21:** Added "Average Speed Exceeded vs Weather Condition" and "Average Fine Amount by Violation Type" visualizations to the Data Visualization page.
* **2025-11-20:** Fixed a bug in the Numerical Analysis page that caused a `pyarrow.lib.ArrowInvalid` error when displaying dataset statistics for columns containing dates.
