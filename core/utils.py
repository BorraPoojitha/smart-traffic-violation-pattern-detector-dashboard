import pandas as pd


# =================================================================================
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
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

    #===================
    # More refiners if required
    # ==================
    return df
# =================================================================================
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
    return filtered_df
# =================================================================================
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
# =================================================================================
