import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
import core.trend_plot as trend_plot
import core.visualize_plot as visualize_plot
import matplotlib.pyplot as plt

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Trend Analysis - Smart Traffic Violation Pattern Detector Dashboard", 
    page_icon="📈", 
    layout="wide"
)
st.title("📈 Trend Analysis")
st.markdown("Analyze trends over time based on different categories.")

# ===============================================================================================
# QUICK NAVIGATOR
# ===============================================================================================
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

        .nav-pill-custom {
            background: rgba(245, 158, 11, 0.3);
            border-color: rgba(245, 158, 11, 0.5);
            text-decoration: none !important;
        }

        .nav-pill-custom:hover {
            background: rgba(245, 158, 11, 0.5);
            border-color: rgba(245, 158, 11, 0.7);
            color: #ffffff !important;
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
            .nav-links {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <div class="nav-container">
        <div class="nav-header"> Trend Navigator</div>
        <div class="nav-links">
            <a class="nav-pill" href="#time-series-analysis" target="_self">Time Series</a>
            <a class="nav-pill" href="#financial-impact-analysis" target="_self">Financial Impact</a>
            <a class="nav-pill" href="#severity-and-risk-analysis" target="_self">Severity & Risk</a>
            <a class="nav-pill nav-pill-custom" href="#custom-trend-exploration" target="_self">Custom Analysis</a>
        </div>
    </div>
    """

st.sidebar.markdown(quick_navigator, unsafe_allow_html=True)
st.markdown(quick_navigator, unsafe_allow_html=True)
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

# ===============================================================================================
# --- Hardcoded Trend Plots ---
# ===============================================================================================
def render_hardcoded_trend_plots(df):
    """
    Renders hardcoded trend plots: Month vs Violation Type and Year vs Violation Type to Separate Controls.
    """
    # Ensure Date column exists and is datetime
    if 'Date' not in df.columns:
         return
    
    # Create working copy
    df_plot = df.copy()
    df_plot['Date'] = pd.to_datetime(df_plot['Date'], errors='coerce')
    df_plot = df_plot.dropna(subset=['Date'])
    
    if df_plot.empty:
        st.warning("No valid dates found for trend plotting.")
        return

    # --- Helper Function for Independent Sections ---
    def render_single_trend_section(dataset, timeframe_col, title, key_suffix, plot_func_x_label):
        st.markdown(f"### {title}")
        
        # Default Filter Values
        try:
            min_date = dataset['Date'].min().date()
            max_date = dataset['Date'].max().date()
        except:
             min_date, max_date = None, None
        
        all_violation_types = sorted(dataset['Violation_Type'].dropna().unique())

        # Form for Controls
        with st.expander(f"Configure {title}", expanded=False):
            with st.form(key=f"form_{key_suffix}"):
                # Date Range
                if min_date and max_date:
                    c1, c2 = st.columns(2)
                    with c1:
                         start_d = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date, key=f"start_{key_suffix}")
                    with c2:
                         end_d = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date, key=f"end_{key_suffix}")
                else:
                    start_d, end_d = None, None

                # 4:1 Layout for Multiselect : Submit Button
                c_sel, c_btn = st.columns([4, 1])
                with c_sel:
                    sel_viol = st.multiselect(
                        "Filter by Violation Type", 
                        options=all_violation_types,
                        default=None,
                        key=f"viol_{key_suffix}"
                    )
                with c_btn:
                    # Align button to bottom to match input height roughly or just center vertically
                    st.write("") # Spacer
                    st.write("") 
                    submit = st.form_submit_button("Update Plot", type="primary")

        # --- Filtering Logic ---
        # Note: In Streamlit forms, the script basically re-runs on submit. 
        # The values `sel_viol`, `start_d` etc. are updated.

        # Filter Date
        data_filtered = dataset.copy()
        if start_d and end_d:
            if start_d > end_d:
                st.error("End Date must be after Start Date")
                return
            data_filtered = data_filtered[(data_filtered['Date'].dt.date >= start_d) & (data_filtered['Date'].dt.date <= end_d)]

        # Filter Violation
        if sel_viol:
            data_filtered = data_filtered[data_filtered['Violation_Type'].isin(sel_viol)]

        if data_filtered.empty:
            st.info(f"No data available for {title} with current filters.")
            return

        # --- Plotting Logic ---
        if timeframe_col == 'Month':
            data_filtered['Month'] = data_filtered['Date'].dt.month_name()
            counts = data_filtered.groupby(['Month', 'Violation_Type']).size().reset_index(name='Count')
            if not counts.empty:
                pivot_data = counts.pivot(index='Month', columns='Violation_Type', values='Count').fillna(0)
                month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                pivot_data = pivot_data.reindex(month_order).dropna()
                fig = trend_plot.plot_trend_analysis_line(pivot_data, plot_func_x_label, "Violation_Type")
                st.pyplot(fig, width='stretch')
            else:
                st.info("No data to plot.")

        elif timeframe_col == 'Year':
            data_filtered['Year'] = data_filtered['Date'].dt.year
            counts = data_filtered.groupby(['Year', 'Violation_Type']).size().reset_index(name='Count')
            if not counts.empty:
                pivot_data = counts.pivot(index='Year', columns='Violation_Type', values='Count').fillna(0)
                fig = trend_plot.plot_trend_analysis_line(pivot_data, plot_func_x_label, "Violation_Type")
                st.pyplot(fig, width='stretch')
            else:
                 st.info("No data to plot.")

    # 1. Monthly Trend Section
    render_single_trend_section(df_plot, 'Month', "Monthly Trend by Violation Type", "monthly", "Month")
    st.markdown("---")

    # 2. Yearly Trend Section
    render_single_trend_section(df_plot, 'Year', "Yearly Trend by Violation Type", "yearly", "Year")
    st.markdown("---")

# ===============================================================================================
# --- MOVED LINE PLOTS (FROM VISUALIZE DATA) ---
# ===============================================================================================

def render_plot_item(title, insight, plot_func, team_member_name, df_local, key_suffix):
    """
    Renders a single plot item in an expander with independent date filtering.
    """
    st.markdown(f"### {title}")
    
    expander_title = f"{title}"
    
    with st.expander(expander_title, expanded=True):
        try:
            plt.close('all')
        except:
            pass

        key_start = f"start_{key_suffix}"
        key_end = f"end_{key_suffix}"
        
        filtered_df = df_local.copy()
        
        min_d, max_d = None, None
        if 'Date' in df_local.columns:
            try:
                temp_dates = pd.to_datetime(df_local['Date'], errors='coerce').dropna()
                if not temp_dates.empty:
                    min_d = temp_dates.min().date()
                    max_d = temp_dates.max().date()
            except:
                pass

        s_date, e_date = None, None
        if min_d and max_d:
            c1, c2 = st.columns(2)
            with c1:
                s_date = st.date_input("Start Date", min_d, min_value=min_d, max_value=max_d, key=key_start)
            with c2:
                e_date = st.date_input("End Date", max_d, min_value=min_d, max_value=max_d, key=key_end)
            
            if s_date and e_date:
                if s_date > e_date:
                    st.error("Start Date must be before End Date.")
                else:
                    if filtered_df['Date'].dtype == 'object':
                            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors='coerce')
                    
                    filtered_df = filtered_df[
                        (filtered_df['Date'].dt.date >= s_date) & 
                        (filtered_df['Date'].dt.date <= e_date)
                    ]
        
        if filtered_df.empty:
            st.warning("No data available for the selected range.")
        else:
            total_records = len(filtered_df)
            date_range_str = f"`{s_date}` to `{e_date}`" if s_date and e_date else "All Time"

            col_plot, col_insight = st.columns([4, 1])
            
            with col_plot:
                try:
                    fig = plot_func(filtered_df)
                    if fig:
                        st.pyplot(fig, width='stretch')
                    else:
                        st.write("Plot could not be generated.")
                except Exception as e:
                    st.error(f"Error generating plot: {e}")
            
            with col_insight:
                st.markdown("#### Statistics")
                st.metric("Total Records", total_records, help=f"Created by: {team_member_name}")
                st.write("Date Range:")
                st.write(date_range_str)
                st.divider()
                st.info(f"**💡 Insight:**\n\n{insight}")
            
            st.markdown("---")



# ===============================================================================================
# --- Custom Trend Line Plot ---
# ===============================================================================================
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

        # --- New Filter & Plot Type Section ---
        col_filter, col_plot_type = st.columns([3, 1])
        
        with col_filter:
            with st.expander(f"Filter by {Lines} (Optional)", expanded=False):
                 unique_values = df[Lines].dropna().unique()
                 selected_filter_values = st.multiselect(f"Select specific {Lines} to display", unique_values, key="trend_filter_val")
        
        with col_plot_type:
            with st.expander("Plot Type", expanded=False):
                plot_type = st.radio("Select Plot Type", ["Matplotlib", "Streamlit Default"],)

        col1, col2 = st.columns([5,1])
        with col2:
            generate_button = st.button("Generate Trend Plot", type="primary")

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

            # --- Apply Multi-Filter ---
            if selected_filter_values:
                df_filtered = df_filtered[df_filtered[Lines].isin(selected_filter_values)]

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

            st.markdown(f"## `{Lines.replace('_',' ').title()}` Trend based on `{X_axis.replace('_',' ').title()}`")
            st.markdown(f"##### Date Range: `{start_date}` to `{end_date}`")

            if plot_type == "Matplotlib":
                fig = trend_plot.plot_trend_analysis_line(attribute_based_pivot, X_axis, Lines)
                st.pyplot(fig, width='stretch')
            elif plot_type == "Streamlit Default":
                st.line_chart(attribute_based_pivot,width='stretch',x_label= X_axis, y_label="Count")
            else:
                st.info("Coming Soon!")
            with st.expander("View Plotted Data"):
                st.dataframe(attribute_based_pivot)
        else:
            st.info("Configure the plot options above and click 'Generate Trend Plot' to see the analysis.")

# ===============================================================================================
# --- Categorical Heatmap ---
# ===============================================================================================
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



# ===============================================================================================
# --- MAIN EXECUTION ---
# ===============================================================================================

# 1. TIME SERIES
st.markdown('<h2 id="time-series-analysis" style="text-align: center;">Time Series Analysis</h3>', unsafe_allow_html=True)
render_hardcoded_trend_plots(df)
render_plot_item(
    "Peak Hour Traffic", 
    "Identifies the time of day with the highest traffic volume and violations.",
    visualize_plot.plot_peak_hour_traffic,
    "Rakshitha", df, "rakshitha_1_moved"
)
st.markdown("---")

# 2. FINANCIAL IMPACT
st.markdown('<h2 id="financial-impact-analysis" style="text-align: center;">Financial Impact Analysis</h3>', unsafe_allow_html=True)
render_plot_item(
    "Total Fines Per Year", 
    "Tracks revenue trends over time, indicating changes in enforcement or violation frequency.",
    visualize_plot.plot_fines_per_year,
    "Amith", df, "amith_2_moved"
)
render_plot_item(
    "Avg Fine by Location", 
    "Compares the average fine amount collected across different geographic locations.",
    visualize_plot.plot_avg_fine_location_line,
    "Ishwari", df, "ishwari_2_moved"
)
st.markdown("---")

# 3. SEVERITY & RISK
st.markdown('<h2 id="severity-risk-analysis" style="text-align: center;">Severity & Risk Analysis</h3>', unsafe_allow_html=True)
render_plot_item(
    "Driver Risk by Age Group", 
    "Demographic analysis showing which age groups are considered higher risk.",
    visualize_plot.plot_driver_risk_by_age,
    "Saniya", df, "saniya_2_moved"
)
st.markdown("---")

# 4. CUSTOM
st.markdown('<h2 id="custom-trend-exploration" style="text-align: center;">Custom Trend Exploration</h3>', unsafe_allow_html=True)
# Render Custom Trend Line Plots
render_trend_analysis_line_plot_section()
st.markdown("---")
# Render Custom Categorical Heatmap
render_categorical_heatmap_section()
st.markdown("---")