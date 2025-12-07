import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from core import map_plot
"""
All Fields in the dataset:
    Violation_ID                  object
    Violation_Type                object
    Fine_Amount                    int64
    Location                      object
    Date                          object
    Time                          object
    Vehicle_Type                  object
    Vehicle_Color                 object
    Vehicle_Model_Year             int64
    Registration_State            object
    Driver_Age                     int64
    Driver_Gender                 object
    License_Type                  object
    Penalty_Points                 int64
    Weather_Condition             object
    Road_Condition                object
    Officer_ID                    object
    Issuing_Agency                object
    License_Validity              object
    Number_of_Passengers           int64
    Helmet_Worn                   object
    Seatbelt_Worn                 object
    Traffic_Light_Status          object
    Speed_Limit                    int64
    Recorded_Speed                 int64
    Alcohol_Level                float64
    Breathalyzer_Result           object
    Towed                         object
    Fine_Paid                     object
    Payment_Method                object
    Court_Appearance_Required     object
    Previous_Violations            int64
    Comments                      object
"""
# ==================================================================================
# Block 0: Basic and Classic Data Processing Functions
# ==================================================================================
def filter_the_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
        Violation_ID                  object
        Violation_Type                object
        Fine_Amount                    int64
        Location                      object
        Date                          object
        Time                          object
        Vehicle_Type                  object
        Vehicle_Color                 object
        Vehicle_Model_Year             int64
        Registration_State            object
        Driver_Age                     int64
        Driver_Gender                 object
        License_Type                  object
        Penalty_Points                 int64
        Weather_Condition             object
        Road_Condition                object
        Officer_ID                    object
        Issuing_Agency                object
        License_Validity              object
        Number_of_Passengers           int64
        Helmet_Worn                   object
        Seatbelt_Worn                 object
        Traffic_Light_Status          object
        Speed_Limit                    int64
        Recorded_Speed                 int64
        Alcohol_Level                float64
        Breathalyzer_Result           object
        Towed                         object
        Fine_Paid                     object
        Payment_Method                object
        Court_Appearance_Required     object
        Previous_Violations            int64
        Comments                      object
    """
    # Date and Time Filteration
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce', format='mixed')

    #===================
    # More refiners if required
    # ==================
    return df
# -------------------------------------------------------------------------------
def get_last_n_days_data(df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Filters the DataFrame to include only records from the last n days.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'Date' column.
        n (int): The number of days to look back from today.

    Returns:
        pd.DataFrame: A filtered DataFrame with records from the last n days.
    """
    today = pd.Timestamp.now().normalize()
    n_days_ago = today - pd.Timedelta(days=n)
    filtered_df = df[(df['Date'] >= n_days_ago) & (df['Date'] <= today)]
    return filtered_df.copy()
# ----------------------------------------------------------------------------
def find_location_columns(df, known_locations, sample_size=20, threshold=0.8) -> list:
    """
    Analyzes a DataFrame to find columns that likely contain location names.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        known_locations (set): A set of known location names (e.g., from a GeoJSON file), in lowercase.
        sample_size (int): The number of unique values to sample from each column.
        threshold (float): The percentage of matches required to consider a column as a location column (0.0 to 1.0).

    Returns:
        list: A list of column names that are likely location columns.
    """
    potential_location_cols = []
    
    # Consider only object/categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        # Drop nulls and get unique values
        unique_values = df[col].dropna().unique()
        
        if len(unique_values) == 0:
            continue
            
        # Take a sample to check against
        sample = unique_values[:sample_size]
        
        match_count = 0
        for val in sample:
            if isinstance(val, str) and val.lower() in known_locations:
                match_count += 1
        
        # Calculate match percentage
        match_percentage = match_count / len(sample)
        
        if match_percentage >= threshold:
            potential_location_cols.append(col)
            
    return potential_location_cols
# ===================================================================================


# ==================================================================================
# Block 1: Data Quality Analysis Functions
# ===================== Data Quality Analysis Functions ============================

def get_data_quality_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates missing, unique, and duplicate statistics for each column.
    
    Returns:
        pd.DataFrame: A formatted DataFrame with percentage metrics.
    """
    total_rows = len(df)
    report = []
    
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        unique_count = df[col].nunique()
        redundant_count = total_rows - unique_count
        
        # present_pct = ((total_rows - missing_count) / total_rows) * 100
        missing_pct = (missing_count / total_rows) * 100
        unique_pct = (unique_count / total_rows) * 100
        duplicate_pct = (redundant_count / total_rows) * 100
        
        # Outlier Calculation (IQR Method) for numeric columns
        outlier_pct = 0.0
        if pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_pct = (len(outliers) / total_rows) * 100

        report.append({
            'Column Name': col,
            # 'Present (%)': round(present_pct, 2),
            'Missing (%)': round(missing_pct, 2),
            'Unique (%)': round(unique_pct, 2),
            'Duplicate (%)': round(duplicate_pct, 2),
            'Outlier (%)': round(outlier_pct, 2)
        })
        

    return pd.DataFrame(report)

# ===================== End of Data Quality Analysis Functions =====================


# ==================================================================================
# Block 2: Numerical Analysis Functions (Tabular/Grouped)
# ===================== Numerical Analysis Functions ===============================

def get_violation_stats_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates Fine Amount by Violation Type (Count, Sum, Mean, Min, Max).
    """
    if 'Violation_Type' not in df.columns or 'Fine_Amount' not in df.columns:
        return pd.DataFrame()
    
    stats = df.groupby('Violation_Type')['Fine_Amount'].agg(['count', 'sum', 'mean', 'min', 'max']).reset_index()
    stats.columns = ['Violation Type', 'Total Incidents', 'Total Fines', 'Average Fine', 'Min Fine', 'Max Fine']
    stats = stats.sort_values(by='Total Fines', ascending=False)
    return stats
# -------------------------------------------------------------------------------
def get_demographic_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a pivot table of Violation Counts by Violation Type (Rows) and Driver Gender (Columns).
    """
    if 'Violation_Type' not in df.columns or 'Driver_Gender' not in df.columns:
        return pd.DataFrame()
    
    pivot = df.pivot_table(index='Violation_Type', columns='Driver_Gender', values='Violation_ID', aggfunc='count', fill_value=0)
    pivot['Total'] = pivot.sum(axis=1)
    pivot = pivot.sort_values(by='Total', ascending=False)
    return pivot
# -------------------------------------------------------------------------------
def get_vehicle_analysis_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates fines and counts by Vehicle Type and Model Year.
    """
    cols_needed = ['Vehicle_Type', 'Vehicle_Model_Year', 'Fine_Amount']
    if not all(col in df.columns for col in cols_needed):
        return pd.DataFrame()
        
    stats = df.groupby(['Vehicle_Type', 'Vehicle_Model_Year'])['Fine_Amount'].agg(['count', 'mean']).reset_index()
    stats.columns = ['Vehicle Type', 'Model Year', 'Violation Count', 'Avg Fine']
    stats = stats.sort_values(by='Violation Count', ascending=False)
    return stats
# -------------------------------------------------------------------------------
def get_speeding_analysis_by_zone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes speeding violations grouped by Speed Limit zones.
    """
    cols_needed = ['Speed_Limit', 'Recorded_Speed']
    if not all(col in df.columns for col in cols_needed):
        return pd.DataFrame()
    
    df_speed = df.copy()
    df_speed['Excess_Speed'] = df_speed['Recorded_Speed'] - df_speed['Speed_Limit']
    df_speed = df_speed[df_speed['Excess_Speed'] > 0] # Only actual speeding
    
    if df_speed.empty:
        return pd.DataFrame()

    stats = df_speed.groupby('Speed_Limit')['Excess_Speed'].agg(['count', 'mean', 'max']).reset_index()
    stats.columns = ['Speed Limit Zone', 'Speeding Incidents', 'Avg Excess Speed', 'Max Excess Speed']
    return stats
# -------------------------------------------------------------------------------
def get_environmental_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Grouped analysis of violations by Weather Condition and Road Condition.
    """
    cols_needed = ['Weather_Condition', 'Road_Condition']
    if not all(col in df.columns for col in cols_needed):
        return pd.DataFrame()
        
    stats = df.groupby(['Weather_Condition', 'Road_Condition']).size().reset_index(name='Violation Count')
    stats = stats.sort_values(by='Violation Count', ascending=False)
    return stats
# -------------------------------------------------------------------------------
def get_hourly_patterns_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot table of Violation Counts by Day of Week vs Hour of Day.
    """
    if 'Time' not in df.columns or 'Date' not in df.columns:
        return pd.DataFrame()
        
    temp_df = df.copy()
    # Fix UserWarning: parse dates/times with format='mixed' to handle inconsistencies
    temp_df['Hour'] = pd.to_datetime(temp_df['Time'], format='mixed', errors='coerce').dt.hour
    temp_df['Day'] = pd.to_datetime(temp_df['Date'], format='mixed', errors='coerce').dt.day_name()
    
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    temp_df['Day'] = pd.Categorical(temp_df['Day'], categories=days_order, ordered=True)
    
    # Fix FutureWarning: specify observed=False for categorical data
    pivot = temp_df.pivot_table(index='Day', columns='Hour', values='Violation_ID', aggfunc='count', fill_value=0, observed=False)
    return pivot
# -------------------------------------------------------------------------------
def get_custom_grouping(df: pd.DataFrame, group_cols: list, agg_cols: list, agg_funcs: list) -> pd.DataFrame:
    """
    Dynamically groups the dataframe based on user input.
    """
    if not group_cols or not agg_cols or not agg_funcs:
        return pd.DataFrame()
    
    # Create the aggregation dictionary: apply all selected functions to all selected numerical columns
    agg_dict = {col: agg_funcs for col in agg_cols}
    
    try:
        grouped_df = df.groupby(group_cols).agg(agg_dict).reset_index()
        
        # Flatten MultiIndex columns (e.g., ('Fine_Amount', 'sum') -> 'Fine_Amount_sum')
        new_cols = []
        for col in grouped_df.columns:
            if isinstance(col, tuple):
                 # Skip the grouping columns if they happen to be part of the index/tuple structure in some pandas versions,
                 # but usually reset_index handles grouping cols nicely.
                 # The aggregated columns will be tuples like ('Fine_Amount', 'mean')
                 if col[1] == '':
                     new_cols.append(col[0])
                 else:
                     new_cols.append(f"{col[0]}_{col[1]}")
            else:
                new_cols.append(col)
        
        grouped_df.columns = new_cols
        return grouped_df
    except Exception as e:
        print(f"Grouping Error: {e}")
        return pd.DataFrame()

# ===================== End of Numerical Analysis Functions ========================



# Block 4: Map Visualization Functions
# ========================= Map Visualization Functions ==========================

def render_choropleth_map_on_page(map_data, geojson_data, location_col, value_col, state_prop_name, color_theme="YlGnBu", title="Map"):
    """
    Renders a Folium Choropleth map using the core module and displays it on Streamlit.
    """
    if map_data is None or map_data.empty:
        st.warning(f"No data available for {title}.")
        return

    # Capitalize location names
    map_data[location_col] = map_data[location_col].str.title()

    # 4:1 Column Layout
    col1, col2 = st.columns([3, 1],border=True)
    
    with col1:
        # Custom Legend for "No Data" - Positioned Top Right
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: flex-end; margin-bottom: 5px;">
                <div style="width: 20px; height: 20px; background-color: gray; opacity: 0.4; margin-right: 10px; border: 1px solid #ccc;"></div>
                <span>No Data Found (Gray)</span>
            </div>  
        """, unsafe_allow_html=True)

        # Generate Map Object using core Logic
        m = map_plot.plot_choropleth_map(map_data, geojson_data, location_col, value_col, state_prop_name, color_theme)
        st_folium(m, width='stretch', height=500, key=f"map_{title.replace(' ', '_')}", returned_objects=[])

    with col2:
        # Metric: Should be different for different types of maps representing different data
        # for violation -> show Total Violations(Sum)
        # for Fine Amount -> show Total Fine Amount Rs.(Sum)
        # For Driver's Age -> show Total Drivers(Avg)

        if pd.api.types.is_numeric_dtype(map_data[value_col]) and title == "Violations Count":
            total_val = map_data[value_col].sum()
            st.metric(label="Total Violations Count", value=f"{total_val:,.0f}")

        elif pd.api.types.is_numeric_dtype(map_data[value_col]) and  title == "Total Fines Generated":
            total_val = map_data[value_col].sum()
            st.metric(label="Total Fine Amount (Rs.)", value=f"Rs. {total_val:,.0f}")
        
        elif pd.api.types.is_numeric_dtype(map_data[value_col]) and  title == "Average Driver's Age":
            mean_age_of_all_locations = map_data[value_col].mean()
            st.metric(label="Overall Average Age:", value=f"{mean_age_of_all_locations:,.0f} Years")

        else:
            total_count = map_data.shape[0]
            st.metric(label="Total Records", value=total_count, border=True)

        # Top 5 Locations Table
        st.caption(f"Top 5 {location_col.title()}s")
        top_5 = map_data.sort_values(by=value_col, ascending=False).head(5)
        st.dataframe(top_5, hide_index=True, width='stretch')
        
        # View Full Data Expander
        with st.expander("Full Data"):
            st.dataframe(map_data, hide_index=True, width='stretch')

# ===================== End of Map Visualization Functions =======================