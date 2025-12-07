import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
import core.visualize_plot as visualize_plot
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Data Visualization - Smart Traffic Violation Pattern Detector Dashboard", 
    page_icon="🎨", 
    layout="wide"
)

st.title("🎨 Data Visualization")
st.markdown("Explore relationships and distributions in your data using various plots.")

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

        /* Responsive - single column on very narrow screens */
        @media (max-width: 300px) {
            .nav-links {
                grid-template-columns: 1fr;
            }
            
            .nav-pill {
                font-size: 0.8rem;
                padding: 8px 10px;
                min-height: 40px;
            }
        }

        /* For wider sidebars or main content */
        @media (min-width: 500px) {
            .nav-container {
                padding: 20px;
            }
            
            .nav-header {
                font-size: 1.2rem;
                margin-bottom: 16px;
            }
            
            .nav-links {
                gap: 12px;
            }
            
            .nav-pill {
                padding: 12px 16px;
                font-size: 0.9rem;
                min-height: 48px;
            }
        }
    </style>

    <div class="nav-container">
        <div class="nav-header">Quick Navigator</div>
        <div class="nav-links">
            <a class="nav-pill" href="#locations-analysis" target="_self">Locations</a>
            <a class="nav-pill" href="#vehicle-insights" target="_self">Vehicles</a>
            <a class="nav-pill" href="#fines-and-trends" target="_self">Fines & Trends</a>
            <a class="nav-pill" href="#severity-and-risk-analysis" target="_self">Risk and ..</a>
            <a class="nav-pill" href="#environmental-and-road-analysis" target="_self">Environmental</a>
            <a class="nav-pill nav-pill-custom" href="#custom-visualizations" target="_self">Custom</a>
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
        st.warning("No dataset selected. Please select one from the sidebar.")
        st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

# ===========================================================================================
# TEAM CONTRIBUTED PLOTS
# ===========================================================================================

def render_plot_item(title, insight, plot_func, team_member_name, df_local, key_suffix):
    """
    Renders a single plot item in an expander with independent date filtering.
    """
    # Navigation Anchor
    st.markdown(f"### {title}")
    
    expander_title = f"{title}"
    
    with st.expander(expander_title, expanded=True):
        # Ensure fresh state for plots
        try:
            plt.close('all')
        except:
            pass

        # --- Date Filter for this SPECIFIC Plot ---
        key_start = f"start_{key_suffix}"
        key_end = f"end_{key_suffix}"
        
        filtered_df = df_local.copy()
        
        # Determine min/max date if possible
        min_d, max_d = None, None
        if 'Date' in df_local.columns:
            try:
                temp_dates = pd.to_datetime(df_local['Date'], errors='coerce').dropna()
                if not temp_dates.empty:
                    min_d = temp_dates.min().date()
                    max_d = temp_dates.max().date()
            except:
                pass

        # Date Inputs
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

            # Uniform Layout: Plot (Large) | Insight (Small) -> 4 : 1
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
                st.markdown("#### 📊 Statistics")
                st.metric("Total Records", total_records)
                st.write("Date Range:")
                st.write(date_range_str)
                st.divider()
                st.info(f"**Insight:**\n\n{insight}")
            


# ===========================================================================================
# 📍 LOCATIONS
# ===========================================================================================
st.markdown("---")
st.markdown('<h2 id="top-5-locations-violations" style="text-align: center;">Locations Analysis</h3>', unsafe_allow_html=True)

render_plot_item(
    "Top 5 Locations (Violations)", 
    "Identifies the highest-risk areas with the most violations, useful for targeted enforcement.",
    visualize_plot.plot_top_5_locations_violation,
    "Monika", df, "monika_1"
)

render_plot_item(
    "Violations by Location (%)", 
    "Shows the geographical distribution of violations to pinpoint hotspots.",
    visualize_plot.plot_violation_by_location_pie,
    "Harika", df, "harika_2"
)



# ===========================================================================================
# 🚗 VEHICLES
# ===========================================================================================
st.markdown("---")
st.markdown('<h2 id="vehicle-type-vs-violation-type" style="text-align: center;">Vehicle Insights</h3>', unsafe_allow_html=True)

render_plot_item(
    "Vehicle Type vs Violation Type", 
    "Correlates vehicle categories with specific violation behaviors to understand offender profiles.",
    visualize_plot.plot_vehicle_type_vs_violation_type,
    "Monika", df, "monika_2"
)

render_plot_item(
    "Vehicle Risk Analysis", 
    "Assesses which vehicle types are most prone to accumulating violations.",
    visualize_plot.plot_vehicle_risk_countplot,
    "Sanjana", df, "sanjana_1"
)

render_plot_item(
    "Fine Paid vs Vehicle Type", 
    "Shows the distribution of total fines paid across different vehicle categories.",
    visualize_plot.plot_fine_vs_vehicle_pie,
    "Ishwari", df, "ishwari_1"
)

# ===========================================================================================
# 💰 FINES
# ===========================================================================================
st.markdown("---")
st.markdown('<h2 id="total-fines-per-year" style="text-align: center;">Fines & Trends</h3>', unsafe_allow_html=True)



render_plot_item(
    "Fine Amount by Violation Type", 
    "Compares the average financial penalty associated with different violation categories.",
    visualize_plot.plot_avg_fine_by_violation_type_2,
    "Poojitha", df, "poojitha_2"
)

render_plot_item(
    "Fine Amount vs Weather (Violin Plot)", 
    "Visualizes the distribution of fine amounts across various weather conditions.",
    visualize_plot.plot_fine_amount_distribution_vs_weather,
    "Anshu", df, "anshu_1"
)

render_plot_item(
    "Violation Type Percentage", 
    "Shows the breakdown of violation types, highlighting the most common infractions.",
    visualize_plot.plot_violation_type_percentage,
    "Amith", df, "amith_1"
)

# ===========================================================================================
# 🔥 RISK & DEMOGRAPHICS
# ===========================================================================================
st.markdown("---")
st.markdown('<h2 id="severity-and-risk-analysis" style="text-align: center;">Risk & Demographics Analysis</h3>', unsafe_allow_html=True)

render_plot_item(
    "Violation Severity Heatmap", 
    "Visualizes the intensity of violations across locations based on a severity score.",
    visualize_plot.plot_severity_heatmap_by_location,
    "Mrunalini", df, "mrunalini_1"
)

render_plot_item(
    "Repeat Offenders", 
    "Highlights drivers with multiple violations, crucial for identifying habitual offenders.",
    visualize_plot.plot_repeat_offenders,
    "Harika", df, "harika_1"
)



render_plot_item(
    "Age vs Alcohol Heatmap", 
    "Correlates driver age with alcohol-related incidents to identify at-risk demographics.",
    visualize_plot.plot_age_alcohol_heatmap,
    "Sanjana", df, "sanjana_2"
)

render_plot_item(
    "License Validity by Gender", 
    "Breakdown of license status (Valid/Expired) by driver gender.",
    visualize_plot.plot_license_validity_by_gender,
    "Anshu", df, "anshu_2"
)

# ===========================================================================================
# 🌍 ENVIRONMENTAL & ROAD IMPACT
# ===========================================================================================
st.markdown("---")
st.markdown('<h2 id="environmental-and-road-analysis" style="text-align: center;">Environmental & Road Analysis</h3>', unsafe_allow_html=True)

render_plot_item(
    "Speeding vs Road Condition", 
    "Analyzes how different road conditions contribute to speeding incidents.",
    visualize_plot.plot_speeding_vs_road_condition,
    "Darsana", df, "darsana_1"
)

render_plot_item(
    "Fines vs Weather (Severity)", 
    "Examines the relationship between weather severity and the magnitude of fines issued.",
    visualize_plot.plot_fines_vs_weather_severity,
    "Darsana", df, "darsana_2"
)

render_plot_item(
    "Speed Exceeded vs Weather", 
    "Shows the tendency to exceed speed limits under various weather conditions.",
    visualize_plot.plot_speed_exceeded_vs_weather_2,
    "Poojitha", df, "poojitha_1"
)

render_plot_item(
    "Violation by Road Condition", 
    "Relates road quality and conditions to the frequency of violations.",
    visualize_plot.plot_violation_by_road_condition,
    "Rakshitha", df, "rakshitha_2"
)

render_plot_item(
    "Weather Impact Heatmap", 
    "Heatmap illustrating how different weather patterns affect violation occurrences.",
    visualize_plot.plot_weather_impact_heatmap,
    "Saniya", df, "saniya_1"
)

render_plot_item(
    "Violation Types vs Weather (Heatmap)", 
    "Correlation between violation types and specific weather conditions.",
    visualize_plot.plot_violation_types_vs_weather_heatmap,
    "Anshu", df, "anshu_3"
)









# ==========================================================================================================    
# CUSTOM VISUALIZATIONS
# ==========================================================================================================    

st.markdown("---")
st.markdown('<h2 id="custom-visualizations" style="text-align: center;">Custom Visualizations</h3>', unsafe_allow_html=True)

st.markdown("### Custom Bar/Count Plot")
with st.expander("Custom Bar/Count Plot", expanded=True):
    st.markdown("Create a bar plot to compare a numerical value across categories, or a count plot for category frequencies.")
    
    # --- Bar Plot Controls ---
    all_categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() < 100]
    all_numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if not all_categorical_cols:
        st.warning("No suitable categorical columns found for the X-axis of a bar plot.")
    else:
        # --- Axis Selectors ---
        col1, col2 = st.columns(2)
        with col1:
            x_col_bar = st.selectbox("Select X-axis (Categorical)", options=all_categorical_cols, key="bar_x")
        with col2:
            y_options = ['Count'] + all_numerical_cols
            y_col_bar = st.selectbox("Select Y-axis (Numerical or Count)", options=y_options, key="bar_y")

        # --- Date Range Selector ---
        bar_start_date, bar_end_date = None, None
        plot_df_bar = df.copy()
        try:
            if 'Date' in df.columns:
                plot_df_bar['Date'] = pd.to_datetime(plot_df_bar['Date'], errors='coerce')
                plot_df_bar.dropna(subset=['Date'], inplace=True)
                if not plot_df_bar['Date'].empty:
                    min_date_bar = plot_df_bar['Date'].min().date()
                    max_date_bar = plot_df_bar['Date'].max().date()
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        bar_start_date = st.date_input("Start date", min_date_bar, min_value=min_date_bar, max_value=max_date_bar, key="bar_start")
                    with c2:
                        bar_end_date = st.date_input("End date", max_date_bar, min_value=min_date_bar, max_value=max_date_bar, key="bar_end")
            else:
                st.info("No 'Date' column found or date conversion failed. Cannot filter by date.")
        except Exception as e:
            st.error(f"Error processing 'Date' column for Bar Plot: {e}")

        if st.button("Generate Bar Plot"):
            # --- Plotting Logic ---
            if bar_start_date and bar_end_date and bar_start_date > bar_end_date:
                st.error("Error: End date must fall after start date.")
            else:
                # Filter by date if applicable
                if bar_start_date and bar_end_date:
                    plot_df_bar = plot_df_bar[(plot_df_bar['Date'].dt.date >= bar_start_date) & (plot_df_bar['Date'].dt.date <= bar_end_date)]
                
                if plot_df_bar.empty:
                    st.warning("No data available for the selected criteria.")
                else:
                    fig = visualize_plot.plot_bar_or_count(plot_df_bar, x_col_bar, y_col_bar)
                    st.pyplot(fig, width='stretch')

                    # Display the underlying data in an expander
                    with st.expander("View Data"):
                        if y_col_bar == 'Count':
                            st.dataframe(plot_df_bar[x_col_bar].value_counts())
                        else:
                            st.dataframe(plot_df_bar.groupby(x_col_bar)[y_col_bar].mean())

# ------------------------------
# CORRELATION ANALYSIS
# ------------------------------
st.markdown("---")
st.markdown("### Custom Correlation Analysis Heatmap Plot")

with st.expander("Custom Correlation Analysis Heatmap Plot", expanded=True):    
    # --- Date Range Selector ---
    corr_start_date, corr_end_date = None, None
    plot_df_corr = df.copy()
    
    date_filter_applied = False
    
    try:
        if 'Date' in df.columns:
            plot_df_corr['Date'] = pd.to_datetime(plot_df_corr['Date'], errors='coerce')
            plot_df_corr.dropna(subset=['Date'], inplace=True)
            if not plot_df_corr['Date'].empty:
                min_date_corr = plot_df_corr['Date'].min().date()
                max_date_corr = plot_df_corr['Date'].max().date()
                
                c1, c2 = st.columns(2)
                with c1:
                    corr_start_date = st.date_input("Start date", min_date_corr, min_value=min_date_corr, max_value=max_date_corr, key="corr_start")
                with c2:
                    corr_end_date = st.date_input("End date", max_date_corr, min_value=min_date_corr, max_value=max_date_corr, key="corr_end")
                date_filter_applied = True
            else:
                st.info("No valid dates found in 'Date' column. Showing correlation for entire dataset.")
        else:
            st.info("No 'Date' column found. Showing correlation for entire dataset.")
    except Exception as e:
        st.error(f"Error processing 'Date' column for Correlation Plot: {e}")

    # Generate Button
    if st.button("Generate Correlation Heatmap"):
        # Filter by date if applicable
        if date_filter_applied and corr_start_date and corr_end_date:
             if corr_start_date > corr_end_date:
                st.error("Error: End date must fall after start date.")
                st.stop()
             plot_df_corr = plot_df_corr[(plot_df_corr['Date'].dt.date >= corr_start_date) & (plot_df_corr['Date'].dt.date <= corr_end_date)]
        
        if plot_df_corr.empty:
            st.warning("No data available for the selected criteria.")
        else:
            # Select only numerical columns for correlation matrix
            numerical_cols = plot_df_corr.select_dtypes(include=['float64', 'int64']).columns
            if len(numerical_cols) < 2:
                st.warning("Not enough numerical columns to generate a correlation matrix.")
            else:
                try:
                    fig = visualize_plot.plot_correlation_heatmap(plot_df_corr, numerical_cols)
                    st.markdown(f"#### Correlation Heatmap (Columns: `{', '.join(numerical_cols)}`)")
                    st.pyplot(fig, width='stretch')
                except Exception as e:
                    st.error(f"An error occurred while generating the heatmap: {e}")

# ------------------------------
# PAIR PLOT SECTION
# ------------------------------
st.markdown("---")
st.markdown("### Custom Pair Plot Analysis")

with st.expander("Pair Plot Analysis", expanded=True):
    # Get numerical and a few categorical columns for selection
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].nunique() < 10]
    selectable_cols = numerical_cols + categorical_cols

    # --- Set new defaults as requested by the user ---
    # Default columns for the pair plot
    user_default_cols = ['Fine_Amount','Vehicle_Model_Year','Speed_Limit','Recorded_Speed','Alcohol_Level','Towed_num','Fine_Paid_num','Court_Appearance_num']
    valid_default_cols = [col for col in user_default_cols if col in selectable_cols]

    # Default column for the hue
    user_default_hue = 'Violation_Type'
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_cols = st.multiselect("Select columns for Pair Plot", options=selectable_cols, default=valid_default_cols)
    with col2:
        hue_options = [None] + categorical_cols
        # Set the default hue if it's a valid option
        hue_index = 0 # Default to None
        if user_default_hue in hue_options:
            hue_index = hue_options.index(user_default_hue)
        selected_hue = st.selectbox("Select column for color (hue)", options=hue_options, index=hue_index)

    if st.button("Generate Pair Plot"):
        if not selected_cols:
            st.error("Please select at least one column to plot.")
        elif len(selected_cols) > 5:
            st.warning("Too many columns selected. Please select 5 or fewer for a clearer plot.")
        else:
            with st.spinner("Generating Pair Plot... This may take a moment."):
                try:
                    # Use a copy of the dataframe for plotting
                    plot_df = df[selected_cols].copy()
                    if selected_hue:
                        plot_df[selected_hue] = df[selected_hue]

                    pair_plot_fig = sns.pairplot(plot_df, hue=selected_hue, corner=True, diag_kind='kde')
                    st.pyplot(pair_plot_fig, width='stretch')
                except Exception as e:
                    st.error(f"An error occurred while generating the pair plot: {e}")
st.markdown("---")