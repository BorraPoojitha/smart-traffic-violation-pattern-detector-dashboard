import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
import core.analysis_plot as analysis_plot

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Numerical Analysis - Smart Traffic Violation Dashboard",
    page_icon="🔢",
    layout="wide",
)
st.title("📊 Numerical Data Analysis Overview")
st.markdown("Dashboard for Data Analysis and Numerical Summary")

# ------------------------------
# LOAD DATA
# ------------------------------
try:
    df_original = render_sidebar()
    if df_original is None:
        st.warning("No dataset selected. Please select one from the sidebar.")
        st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

# ------------------------------
# FILTERS
# ------------------------------
with st.expander("Filters", expanded=True):
    start_date, end_date = None, None
    df = df_original.copy() # Work with a copy

    try:
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            if not df['Date'].empty:
                min_date = df['Date'].min().date()
                max_date = df['Date'].max().date()
                
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start date", min_date, min_value=min_date, max_value=max_date, key="num_start")
                with col2:
                    end_date = st.date_input("End date", max_date, min_value=min_date, max_value=max_date, key="num_end")
            else:
                st.warning("No valid dates found in 'Date' column.")
        else:
            st.info("No 'Date' column available for filtering.")
    except Exception as e:
        st.error(f"Error processing 'Date' column: {e}")
    # Filter the dataframe based on the date range
    if start_date and end_date:
        if start_date > end_date:
            st.error("Error: End date must fall after start date.")
            st.stop()
        df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    else:
        df_filtered = df
    st.write(f"### Showing data for `{df_filtered.shape[0]}` records based on the selected filters.")
st.markdown("---")

# -----------------------------
# DISPLAY BASIC INFORMATION
# ------------------------------





# Display the shape of the dataframe
st.subheader("Dataset Shape")
with st.expander("Dataset Shape", expanded=True):
    st.write(f"The dataset has `{df_filtered.shape[0]}` rows and `{df_filtered.shape[1]}` columns.")
st.markdown("---")

# Display the first 5 rows of the dataframe
st.subheader("5 Sample Rows of the Dataset")
with st.expander("5 Sample Rows", expanded=True):
    st.write(df_filtered.sample(5))
st.markdown("---")

# ------------------------------
# COMBINED DATASET INFORMATION
# ------------------------------
st.header("Combined Dataset Information")
st.write("This section provides a combined view of column names, data types, and descriptive statistics for the filtered data.")
with st.expander("Combined Dataset Information", expanded=True):
    # Create a new dataframe for column information
    info_df = pd.DataFrame({
        'Field': df_filtered.columns,
        'Data Type': df_filtered.dtypes.astype(str)
    }).reset_index(drop=True)

    # Get the descriptive statistics & Merge the two dataframes
    desc_df = df_filtered.describe(include='all').transpose()
    for col in desc_df.columns:
        if desc_df[col].dtype == 'object':
            desc_df[col] = desc_df[col].astype(str)
    desc_df = desc_df.reset_index().rename(columns={'index': 'Field'})
    combined_info = pd.merge(info_df, desc_df, on='Field', how='left')

    st.dataframe(combined_info, width='stretch', hide_index=True)

# ------------------------------
# CORRELATION ANALYSIS
# ------------------------------
st.header("Correlation Analysis")
st.write("This section provides a correlation matrix heatmap for the numerical columns in the filtered dataset.")

# Select only numerical columns for correlation matrix
numerical_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
if len(numerical_cols) < 2:
    st.warning("Not enough numerical columns to generate a correlation matrix.")
else:
    corr_matrix = df_filtered[numerical_cols].corr()

    # Plotting the heatmap

    fig = analysis_plot.plot_correlation_heatmap(df_filtered, numerical_cols)

    st.markdown(f" #### **Heatmap** Columns: `{',`, `'.join(numerical_cols)}'`")
    st.pyplot(fig, width='stretch')

st.markdown("---")

st.markdown("---")
