import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
import core.trend_plot as trend_plot

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="Trend Analysis", page_icon="📈", layout="wide")
st.title("📈 Trend Analysis")
st.markdown("Analyze trends over time based on different categories.")
# ------------------------------
# LOAD DATA
# ------------------------------
try:
    df = render_sidebar()
    if df is None:
        st.warning("No dataset selected or loaded. Please select a dataset from the sidebar.")
        st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

# ------------------------------
# Trend Line Plot
# ------------------------------
def render_trend_analysis_line_plot_section():
    def pre_dataset_test():
        # --- Validate required columns for analysis ---
        x_axis_options = ['Year', 'Month', 'Year_Month', 'Location', 'Vehicle_Type', 'Weather_Condition', 'Road_Condition']
        valid_x_axis_options = [opt for opt in x_axis_options if opt in df.columns or opt in ['Year', 'Month', 'Year_Month']]

        line_options = ['Violation_Type', 'Driver_Gender']
        valid_line_options = [opt for opt in line_options if opt in df.columns]

        if not valid_x_axis_options or not valid_line_options:
            st.warning("Trend analysis is not possible with the current dataset.")
            st.info(
                """
                This analysis requires:
                - A 'Date' column.
                - At least one column for the X-axis (e.g., 'Location', 'Vehicle_Type').
                - At least one column for the trend lines (e.g., 'Violation_Type', 'Driver_Gender').
                """
            )
            st.stop()

        # ------------------------------
        # DATA PREPARATION & VALIDATION
        # ------------------------------
        try:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
        except KeyError:
            st.error("The selected dataset does not have a 'Date' column, which is required for trend analysis.")
            st.stop()

        if df['Date'].empty:
            st.warning("No valid date entries found in the dataset after cleaning.")
            st.stop()

        return valid_x_axis_options, valid_line_options
    
    valid_x_axis_options, valid_line_options = pre_dataset_test()

    with st.expander("Configure Trend Analysis Plot", expanded=True):
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()

        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
            
            default_x_axis = 'Month' if 'Month' in valid_x_axis_options else valid_x_axis_options[0]
            X_axis = st.selectbox("Select X-axis for trend", valid_x_axis_options, index=valid_x_axis_options.index(default_x_axis))

        with col2:
            end_date = st.date_input("End date", max_date, min_value=min_date, max_value=max_date)
            
            default_lines = 'Violation_Type' if 'Violation_Type' in valid_line_options else valid_line_options[0]
            Lines = st.selectbox("Select trend lines (by category)", valid_line_options, index=valid_line_options.index(default_lines))

        generate_button = st.button("Generate Trend Plot")

        if generate_button:
            if start_date > end_date:
                st.error("Error: End date must fall after start date.")
                st.stop()
            
            if Lines is None:
                st.error("No categorical columns available in the dataset to use for trend lines.")
                st.stop()

            start_date_dt = pd.to_datetime(start_date)
            end_date_dt = pd.to_datetime(end_date)
            df_filtered = df[(df['Date'] >= start_date_dt) & (df['Date'] <= end_date_dt)].copy()

            if df_filtered.empty:
                st.warning("No data available for the selected date range.")
                st.stop()

            if X_axis == 'Year':
                df_filtered['Year'] = df_filtered['Date'].dt.year
            elif X_axis == 'Month':
                df_filtered['Month'] = df_filtered['Date'].dt.month_name()
            elif X_axis == "Year_Month":
                df_filtered['Year_Month'] = df_filtered['Date'].dt.to_period('M')

            try:
                attribute_based_counts = df_filtered.groupby([X_axis, Lines]).size().reset_index(name='Count')
            except KeyError:
                st.error(f"The selected columns '{X_axis}' or '{Lines}' are not found in the dataset.")
                st.stop()

            if attribute_based_counts.empty:
                st.warning(f"No data to group for the selected criteria. Try different options.")
                st.stop()

            attribute_based_pivot = attribute_based_counts.pivot(index=X_axis, columns=Lines, values='Count').fillna(0)

            if isinstance(attribute_based_pivot.index, pd.PeriodIndex):
                attribute_based_pivot.index = attribute_based_pivot.index.to_timestamp()

            if X_axis == 'Month':
                month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                attribute_based_pivot = attribute_based_pivot.reindex(month_order).dropna()

            st.markdown("---")
            st.markdown(f"## `{Lines.replace('_',' ').title()}` Trend based on `{X_axis.replace('_',' ').title()}`")
            st.markdown(f"##### Date Range: `{start_date}` to `{end_date}`")

            fig = trend_plot.plot_trend_analysis_line(attribute_based_pivot, X_axis, Lines)
            
            st.pyplot(fig, width='stretch')

            with st.expander("View Plotted Data"):
                st.dataframe(attribute_based_pivot)
        else:
            st.info("Configure the plot options above and click 'Generate Trend Plot' to see the analysis.")

# ----------------------------- 
# Categorical Heatmap
# ----------------------------- 
def render_categorical_heatmap_section():
    st.markdown("## Categorical Analysis Heatmap")
    st.markdown("Analyze the percentage of a specific outcome (e.g., 'Court Appearance Required') across different categories.")

    with st.expander("Configure Categorical Heatmap", expanded=False):
        all_categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() > 1 and df[col].nunique() < 50]
        
        if not all_categorical_cols:
            st.warning("No suitable categorical columns found for this analysis.")
            return

        # --- Prepare date objects if 'Date' column is valid ---
        start_date_cat, end_date_cat = None, None
        min_date_cat, max_date_cat = None, None
        date_filter_available = False
        try:
            if 'Date' in df.columns and not df['Date'].isnull().all():
                min_date_cat = df['Date'].min().date()
                max_date_cat = df['Date'].max().date()
                date_filter_available = True
        except Exception:
            pass # Silently fail if date conversion is not possible

        # --- Controls ---
        col1, col2 = st.columns(2)
        with col1:
            if date_filter_available:
                start_date_cat = st.date_input("Start date", min_date_cat, min_value=min_date_cat, max_value=max_date_cat, key="cat_start")
            
            default_cat_col = 'Court_Appearance_Required' if 'Court_Appearance_Required' in all_categorical_cols else all_categorical_cols[0]
            category_col = st.selectbox("Column to Analyze", all_categorical_cols, index=all_categorical_cols.index(default_cat_col), key="cat_col")

            x_col_options = ['Year', 'Month', 'DayOfWeek']
            x_col = st.selectbox("X-axis", x_col_options, key="cat_x_col")

        with col2:
            if date_filter_available:
                end_date_cat = st.date_input("End date", max_date_cat, min_value=min_date_cat, max_value=max_date_cat, key="cat_end")

            unique_vals = df[category_col].dropna().unique()
            positive_value = st.selectbox("Column Value", options=unique_vals, key="cat_positive_val")

            group_col_options = [col for col in all_categorical_cols if col != category_col]
            if not group_col_options:
                st.warning("Not enough categorical columns to select a different group-by column.")
                group_col = None
            else:
                group_col = st.selectbox("Y-axis (Group by)", group_col_options, key="cat_group_col")

        generate_cat_heatmap = st.button("Generate Categorical Heatmap")

        if generate_cat_heatmap:
            if group_col is None:
                st.error("Please select a Y-axis column.")
                st.stop()
            
            # --- Date Filtering ---
            if date_filter_available and start_date_cat and end_date_cat:
                if start_date_cat > end_date_cat:
                    st.error("Error: End date must fall after start date.")
                    st.stop()
                df_filtered = df[(df['Date'].dt.date >= start_date_cat) & (df['Date'].dt.date <= end_date_cat)].copy()
            else:
                df_filtered = df.copy()

            # --- Merged plotting logic ---
            df_copy = df_filtered
            if x_col in ['Year', 'Month', 'DayOfWeek'] and 'Date' in df_copy.columns:
                # Date conversion already done, just extract parts
                if x_col == 'Year':
                    df_copy[x_col] = df_copy['Date'].dt.year
                elif x_col == 'Month':
                    df_copy[x_col] = df_copy['Date'].dt.month_name()
                elif x_col == 'DayOfWeek':
                    df_copy[x_col] = df_copy['Date'].dt.day_name()

            df_copy['_flag'] = df_copy[category_col].astype(str).str.lower()
            
            totals = df_copy.groupby([group_col, x_col]).size().reset_index(name='Total')
            positive_cases = df_copy[df_copy['_flag'] == str(positive_value).lower()].groupby([group_col, x_col]).size().reset_index(name='Yes')
            
            merged = totals.merge(positive_cases, on=[group_col, x_col], how='left')
            merged['Yes'] = merged['Yes'].fillna(0)
            merged['Percent'] = (merged['Yes'] / merged['Total']) * 100
            
            percent_pivot = merged.pivot(index=group_col, columns=x_col, values='Percent').fillna(0)
            yes_pivot = merged.pivot(index=group_col, columns=x_col, values='Yes').fillna(0)
            
            annot = yes_pivot.astype(int).astype(str) + "\n(" + percent_pivot.round(1).astype(str) + "%)"
            
            fig = trend_plot.plot_categorical_heatmap(percent_pivot, annot, x_col, group_col)
            st.markdown(f"## {category_col} ('{positive_value}') — Count & Percentage Heatmap")
            st.markdown(f"##### Date Range: `{start_date_cat}` to `{end_date_cat}`")
            st.pyplot(fig, width='stretch')
        else:
            st.info("Configure the plot options above and click 'Generate Categorical Heatmap' to see the analysis.")

# --- Render all plots ---
render_trend_analysis_line_plot_section()
st.markdown("---")
render_categorical_heatmap_section()
st.markdown("---")