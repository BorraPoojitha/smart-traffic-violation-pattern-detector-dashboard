import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
from core import utils

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Numerical Analysis - Smart Traffic Violation Pattern Detector Dashboard",
    page_icon="🔢",
    layout="wide",
)

st.header("📋 Detailed Numerical Analysis")
st.markdown("Comprehensive statistical breakdown of the dataset.")

# ===========================================================================================
# QUICK NAVIGATOR
# ===========================================================================================
quick_navigator = """
    <style>
        .nav-container {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.95), rgba(168, 85, 247, 0.95));
            backdrop-filter: blur(10px);
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        .nav-header {
            margin: 0 0 12px 0;
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            text-align: center;
            letter-spacing: -0.3px;
        }

        .nav-links {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }

        .nav-pill {
            text-decoration: none !important;
            background: rgba(255, 255, 255, 0.2);
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px 12px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            white-space: nowrap;
            min-height: 44px;
        }

        .nav-pill:link,
        .nav-pill:visited,
        .nav-pill:hover,
        .nav-pill:active {
            text-decoration: none !important;
        }

        .nav-pill::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }

        .nav-pill:hover::before {
            left: 100%;
        }

        .nav-pill:hover {
            background: rgba(255, 255, 255, 0.35);
            color: #ffffff !important;
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            text-decoration: none !important;
        }

        .nav-pill:active {
            transform: translateY(0) scale(1.01);
            text-decoration: none !important;
        }
        
        /* Dark theme adjustments */
        @media (prefers-color-scheme: dark) {
            .nav-container {
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.98), rgba(168, 85, 247, 0.98));
                border: 1px solid rgba(99, 102, 241, 0.4);
            }
        }

        /* Responsive */
        @media (max-width: 300px) {
            .nav-links { grid-template-columns: 1fr; }
        }
    </style>

    <div class="nav-container">
        <div class="nav-header">Analysis Navigator</div>
        <div class="nav-links">
            <a class="nav-pill" href="#dataset-information" target="_self">Dataset Info</a>
            <a class="nav-pill" href="#violation-type-statistics" target="_self">Violations</a>
            <a class="nav-pill" href="#demographic-analysis" target="_self">Demographics</a>
            <a class="nav-pill" href="#vehicle-and-fine-analysis" target="_self">Vehicles</a>
           <!-- <a class="nav-pill" href="#speeding-analysis-by-zone" target="_self">Speeding</a> -->
            <a class="nav-pill" href="#environmental-impact" target="_self">Environment</a>
            <a class="nav-pill" href="#hourly-violation-patterns" target="_self">Hourly</a>
            <a class="nav-pill" href="#custom-tabular-analysis" target="_self">Custom</a>
        </div>
    </div>
    """

st.sidebar.markdown(quick_navigator, unsafe_allow_html=True)
st.markdown(quick_navigator, unsafe_allow_html=True)

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
    st.write(f"### Showing data for `{df_filtered.shape[0]}`x`{df_filtered.shape[1]}` records based on the selected filters.")
st.markdown("---")

st.markdown('<h2 id="dataset-info" style="text-align: center;">Dataset Information</h3>', unsafe_allow_html=True)

# ==========================================================================================================
# Missing Duplicate Value Analysis
st.subheader('Missing Duplicate Value Analysis')
data_quality_df = utils.get_data_quality_analysis(df)
st.dataframe(data_quality_df, width='stretch', hide_index=True)   

st.markdown('---')     


# Display the first 5 rows of the dataframe
st.subheader("5 Sample Rows of the Dataset")
with st.expander("5 Sample Rows", expanded=True):
    st.write(df_filtered.sample(5))
st.markdown("---")

# ------------------------------
# COMBINED DATASET INFORMATION
# ------------------------------
st.markdown('<h2 id="dataset-info" style="text-align: center;">Combined Dataset Information</h3>', unsafe_allow_html=True)
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
st.markdown("---")

# ===========================================================================================
# DETAILED NUMERICAL ANALYSIS (Tables & GroupBy)
# ===========================================================================================
# ------------------------------------------------------------------------
# 1. Violation Type Statistics
# -------------------------------------------------------------------------
st.markdown('<h2 id="violation-stats" style="text-align: center;">Violation Type Statistics</h3>', unsafe_allow_html=True)
with st.expander("Analysis by Violation Type", expanded=True):
    violation_stats = utils.get_violation_stats_table(df_filtered)
    if not violation_stats.empty:
        # Format currency columns if they exist
        format_dict = {}
        for col in ["Total Fines", "Average Fine", "Min Fine", "Max Fine"]:
            if col in violation_stats.columns:
                format_dict[col] = "Rs. {:,.2f}"
                
        st.dataframe(
            violation_stats.style.format(format_dict),
            width='stretch',
            hide_index=True
        )
    else:
        st.info("Data unavailable for Violation Type analysis.")

# 2. Demographic Pivot
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h2 id="demographic-analysis" style="text-align: center;">Demographic Analysis</h3>', unsafe_allow_html=True)
with st.expander("Gender Distribution by Violation (Pivot Table)", expanded=True):
    demo_pivot = utils.get_demographic_pivot(df_filtered)
    if not demo_pivot.empty:
        st.dataframe(demo_pivot, width='stretch')
    else:
        st.info("Demographic data unavailable.")

# 3. Vehicle Analysis
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h2 id="vehicle-analysis" style="text-align: center;">Vehicle & Fine Analysis</h3>', unsafe_allow_html=True)
with st.expander("Fines by Vehicle Type & Year", expanded=True):
    vehicle_stats = utils.get_vehicle_analysis_table(df_filtered)
    if not vehicle_stats.empty:
        format_dict = {}
        if "Avg Fine" in vehicle_stats.columns:
            format_dict["Avg Fine"] = "Rs. {:,.2f}"
            
        st.dataframe(
            vehicle_stats.style.format(format_dict), 
            width='stretch',
            hide_index=True
        )
    else:
        st.info("Vehicle data unavailable.")

# 4. Speeding Analysis
# -------------------------------------------------------------------------
# st.markdown("---")
# st.markdown('<h2 id="speeding-analysis" style="text-align: center;">Speeding Analysis by Zone</h3>', unsafe_allow_html=True)
# with st.expander("Excess Speed Stats by Limits", expanded=True):
#     speed_stats = utils.get_speeding_analysis_by_zone(df_filtered)
#     if not speed_stats.empty:
#         format_dict = {}
#         if "Avg Excess Speed" in speed_stats.columns:
#             format_dict["Avg Excess Speed"] = "{:.2f} km/h"
#         if "Max Excess Speed" in speed_stats.columns:
#             format_dict["Max Excess Speed"] = "{:.2f} km/h"
            
#         st.dataframe(
#             speed_stats.style.format(format_dict),
#             width='stretch',
#             hide_index=True
#         )
#     else:
#         st.info("No speeding data available.")

# 5. Environmental Impact
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h2 id="environmental-impact" style="text-align: center;">Environmental Impact</h3>', unsafe_allow_html=True)
with st.expander("Violations by Weather & Road Condition", expanded=True):
    env_stats = utils.get_environmental_stats(df_filtered)
    if not env_stats.empty:
        st.dataframe(env_stats, width='stretch', hide_index=True)
    else:
        st.info("Environmental data unavailable.")

# 6. Hourly Patterns
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h2 id="hourly-patterns" style="text-align: center;">Hourly Violation Patterns</h3>', unsafe_allow_html=True)
with st.expander("Day of Week vs Hour (Pivot)", expanded=True):
    hourly_pivot = utils.get_hourly_patterns_table(df_filtered)
    if not hourly_pivot.empty:
        # highlighting max values for better readability in table form
        st.dataframe(hourly_pivot.style.background_gradient(axis=None, cmap="YlOrRd"), width='stretch')
    else:
        st.info("Time Series data unavailable.")

# 7. Custom Analysis
# -------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h2 id="custom-analysis" style="text-align: center;">Custom Tabular Analysis</h3>', unsafe_allow_html=True)
st.markdown("Build your own analysis table by selecting grouping parameters and metrics.")

with st.expander("🛠️ Custom Grouping & Aggregation", expanded=True):
    # Separate columns by type
    cat_cols = df_filtered.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    num_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()

    c1, c2, c3 = st.columns(3)
    with c1:
        selected_group_cols = st.multiselect("1. Select Grouping Columns (Dimensions)", cat_cols)
    with c2:
        selected_agg_cols = st.multiselect("2. Select Aggregation Columns (Metrics)", num_cols)
    with c3:
        selected_funcs = st.multiselect("3. Select Aggregation Functions", ['count', 'sum', 'mean', 'min', 'max', 'std'], default=['count', 'mean'])

    if selected_group_cols and selected_agg_cols and selected_funcs:
        custom_df = utils.get_custom_grouping(df_filtered, selected_group_cols, selected_agg_cols, selected_funcs)
        
        if not custom_df.empty:
            st.write(f"### Resulting Table: {custom_df.shape[0]} rows")
            st.dataframe(custom_df, width='stretch')
            
            # Download button
            csv = custom_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="custom_analysis.csv",
                mime="text/csv",
            )
    else:
        st.info("Please select at least one Grouping Column, one Aggregation Column, and one Function to generate the table.")

st.markdown("---")
