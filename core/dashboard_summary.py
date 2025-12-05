import pandas as pd
import core.dashboard_plot as dashboard_plot

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

# =================================================================================
def get_violations_summary_of_last_n_days(df_last_n_days: pd.DataFrame) -> dict:
    # 1. calculate the no of violations in last n days
    total_no_of_violations = df_last_n_days.shape[0]

    # 2. Generate a figure of barplot for violation types
    fig = dashboard_plot.plot_violation_types_distribution(df_last_n_days, total_no_of_violations)
    
    return {
        'total_no_of_violations': total_no_of_violations,
        'fig': fig
    }

# =================================================================================
def get_total_fines_generated(df_last_n_days: pd.DataFrame) -> dict:
    # 1. calculate total fines in last n days
    total_fines = df_last_n_days['Fine_Amount'].sum()
    avg_fine_per_violation = total_fines / df_last_n_days.shape[0] if df_last_n_days.shape[0] > 0 else 0
    # ==============================================================================
    # 2. Prepare data for fines based on violation type
    df_last_n_days['Fine_Amount'] = pd.to_numeric(df_last_n_days['Fine_Amount'], errors='coerce').fillna(0)
    df_last_n_days['Fine_Paid'] = df_last_n_days['Fine_Paid'].astype(str).str.upper().str.strip()
    summary = (df_last_n_days.groupby(['Violation_Type', 'Fine_Paid'])['Fine_Amount'].sum().unstack(fill_value=0))
    summary = summary.rename(columns={'YES': 'Paid', 'NO': 'Unpaid'})
    
    # 3. Generate a figure of fines based on violation type
    fig = dashboard_plot.plot_fines_based_on_violation_type(summary)
    
    return {
        'total_fines': total_fines,
        'avg_fine_per_violation': avg_fine_per_violation,
        'fig': fig
    }

# =================================================================================
def get_violations_by_location(df_last_n_days: pd.DataFrame) -> dict:
    # 1. No Of Violations for the location
    location_based_violations = df_last_n_days['Location'].value_counts().reset_index()
    location_based_violations.columns = ['Location', 'No of Violations']

    # 2. Total No Of Violations
    total_locations = location_based_violations.shape[0]
    
    # 3. Top Violations Zone
    most_violated_location = location_based_violations.iloc[0]['Location']

    # 4. Plot bar chart for location based violations
    fig = dashboard_plot.plot_violations_by_location(location_based_violations)
    
    return {
        'total_locations': total_locations,
        'most_violated_location': most_violated_location,
        'fig': fig
    }


def get_driver_insights(df_last_n_days: pd.DataFrame) -> dict:
    # 1. Filter out records with missing Driver_Age or Driver_Gender
    df_last_n_days = df_last_n_days.dropna(subset=['Driver_Age', 'Driver_Gender'])  
    df_last_n_days['Driver_Age'] = df_last_n_days['Driver_Age'].astype(int)
    df_last_n_days['Driver_Gender'] = df_last_n_days['Driver_Gender'].astype(str)
    # =================================================================================
    # 2. Calculate insights
    avg_driver_age = df_last_n_days['Driver_Age'].mean().round(2)
    gender_distribution = df_last_n_days['Driver_Gender'].value_counts()
    most_common_gender = gender_distribution.idxmax()
    max_alcohol_level = df_last_n_days['Alcohol_Level'].max()
    # =================================================================================

    # 3. Bar plot for gender distribution
    gender_fig = dashboard_plot.plot_gender_distribution(gender_distribution)

    return {
        'avg_driver_age': avg_driver_age,
        'most_common_gender': most_common_gender,
        'max_alcohol_level': max_alcohol_level,
        'gender_fig': gender_fig
    }
