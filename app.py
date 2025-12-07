import streamlit as st
from core import (
    dashboard_summary,
    utils,
    sidebar,
    data_variables,
    dashboard_plot,
)

# ==========================================================================================================    
# PAGE CONFIG
# ==========================================================================================================    
st.set_page_config(
    page_title="Smart Traffic Violation Dashboard",
    page_icon="🚦",
    layout="wide",
)

def dashboard() -> None:
# ==========================================================================================================    
    # HEADER SECTION
# ==========================================================================================================    
    st.title("🚦 Smart Traffic Violation Summary Dashboard", anchor=False)

# ==========================================================================================================    
    # SIDEBAR
# ==========================================================================================================    
    df = sidebar.render_sidebar()
    if df is None:
        st.warning("No dataset selected. Please select one from the sidebar.")
        st.stop()
    # Filter the dataset
    if set(data_variables.TRAFFIC_VIOLATION_COLUMNS).issubset(set(df.columns)) is False:
        st.warning("Current Dataset is not suitable for this dashboard.")
        st.info(
                f"""
                This analysis requires:
                - A 'Date' column.
                - Require columns like {data_variables.TRAFFIC_VIOLATION_COLUMNS[0], data_variables.TRAFFIC_VIOLATION_COLUMNS[1]} ....
                """
            )
        st.warning("Please Select a valid traffic violation dataset from the sidebar.")
        st.stop()
    elif df.shape[0] == 0:
        st.warning("The selected dataset is empty. Please upload a valid traffic violation dataset.")
        st.stop()
    
    # ==========================================================================================================    
    else:
        # Filter or clean the dataset
        df = utils.filter_the_dataset(df)

# ==========================================================================================================    
    # Summary Calculations for Last N Days
# ==========================================================================================================    
        no_of_days_for_summary  = st.expander("Days Filter", expanded=False).slider("Select Number of Days for Summary Calculations", min_value=7, max_value=365, value=30, step=1, key="days_slider")
        df_last_n_days = utils.get_last_n_days_data(df, no_of_days_for_summary)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"### Total Violations (Last {no_of_days_for_summary} Days)")
            summary = dashboard_summary.get_violations_summary_of_last_n_days(df_last_n_days)
            
            # Display Charts
            # with st.expander("View Violation Types Distribution Chart"):
            with st.container():    
                st.markdown("<h3 style='text-align: center;'>Violation Types Distribution</h3>", unsafe_allow_html=True)
                st.pyplot(summary.get('fig'), width='stretch')
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Total Violations", value=summary.get('total_no_of_violations'))
                
            with sub_col2:
                st.metric(label="Avg Violations/Day", value=f"{int(summary.get('total_no_of_violations')/no_of_days_for_summary)}")
            with sub_col3:
                st.metric(label="Avg Violations/Vehicle", value=f"{int(summary.get('total_no_of_violations')/df_last_n_days['Vehicle_Type'].nunique())}")
            st.markdown('---')
            
    # ==========================================================================================================
            # --- License Insights ---
            st.info(f"### License Insights (Last {no_of_days_for_summary} Days)")
            license_insights = dashboard_summary.get_license_insights(df_last_n_days)
            
            with st.container():
                st.markdown("<h3 style='text-align: center;'>License Validity</h3>", unsafe_allow_html=True)
                st.pyplot(license_insights.get('validity_fig'), width='stretch')
            
            sub_col_l1, sub_col_l2 = st.columns(2, border=True)
            with sub_col_l1:
                st.metric(label="Top License Type", value=license_insights.get('most_common_license_type'))
            with sub_col_l2:
                st.metric(label="Expired License %", value=f"{license_insights.get('expired_percentage')}%")
    # ==========================================================================================================
 
            
    # ==========================================================================================================
        with col2:
            st.info(f"### Total Fines (Last {no_of_days_for_summary} Days)")
            fine_summary = dashboard_summary.get_total_fines_generated(df_last_n_days)
            
            # Display Charts
            # with st.expander("View Fines Distribution Chart"):
            with st.container():    
                st.markdown("<h3 style='text-align: center;'>Fines Distribution</h3>", unsafe_allow_html=True)
                st.pyplot(fine_summary.get('fig'), width='stretch')
            # Metrics
            sub_col1, sub_col2, sub_col3 = st.columns(3, border=True)
            with sub_col1:
                st.metric(label="Total Fines", value=f"Rs.{fine_summary.get('total_fines')}")
            with sub_col2:
                st.metric(label="Average Fines per Day", value=f"Rs.{int(fine_summary.get('total_fines')/no_of_days_for_summary)}")
            with sub_col3:
                st.metric(label="Average Fines per Violation", value=f"Rs.{int(fine_summary.get('avg_fine_per_violation'))}")
            st.markdown('---')

    # ==========================================================================================================
            st.info(f"### Location Insights (Last {no_of_days_for_summary} Days)")
            location_based_summary = dashboard_summary.get_violations_by_location(df_last_n_days)
            # with st.expander("View Violations by Location Chart"):
            with st.container():    
                st.markdown("<h3 style='text-align: center;'>Violations by Location</h3>", unsafe_allow_html=True)
                st.pyplot(location_based_summary.get('fig'), width='stretch')
            # Metrics
            sub_col2, sub_col3 = st.columns(2, border=True)
            
            # with sub_col1:
            #     st.metric(label="Total Locations with Violations", value=location_based_summary.get('total_locations'))
            
            with sub_col2:
                st.metric(label="Most Violated Location", value=location_based_summary.get('most_violated_location'), delta_color='inverse')
            with sub_col3:
                # Integer Division
                avg_violations_per_location = summary.get('total_no_of_violations', 0)//location_based_summary.get('total_locations', 0)
                st.metric(label="Avg Violations/Location", value=f"{avg_violations_per_location}")
        st.markdown('---') 


# ==========================================================================================================  
    # Additional Dashboard Metrics Overview
# ==========================================================================================================  
        # Year Filter for Global Overview
        min_year = int(df['Date'].dt.year.min())
        max_year = int(df['Date'].dt.year.max())
# ==========================================================================================================  
    # GLOBAL DATA OVERVIEW
# ==========================================================================================================  
        st.markdown("<h3 style='text-align: center;'>Global Data Overview</h3>", unsafe_allow_html=True)
        
        # Ensure we have a valid range
        if min_year == max_year:
             selected_years_global = (min_year, max_year)
        else:
             selected_years_global = st.slider(
                 "Filter by Year (Global Overview)",
                 min_value=min_year,
                 max_value=max_year,
                 value=(min_year, max_year),
                 key="slider_global_year"
             )
        
        # Filter Data
        mask_global = (df['Date'].dt.year >= selected_years_global[0]) & (df['Date'].dt.year <= selected_years_global[1])
        df_global = df[mask_global]
        
        with st.expander(f"📊 Executive Summary Report ({selected_years_global[0]} - {selected_years_global[1]})", expanded=True):
             global_metrics = dashboard_summary.get_global_overview_metrics(df_global)
             
             # Row 1
             c1, c2, c3, c4 = st.columns(4, border=True)
             with c1: st.metric("Total Violations", global_metrics.get('total_violations', 0))
             with c2: st.metric("Most Common Violation", global_metrics.get('most_common_violation', 'N/A'))
             with c3: st.metric("Top Location", global_metrics.get('top_location', 'N/A'))
             with c4: st.metric("Top Licensed Agency", global_metrics.get('top_agency', 'N/A'))
             

             
             # Row 2
             c1, c2, c3, c4 = st.columns(4, border=True)
             with c1: st.metric("Avg Fine", f"Rs. {global_metrics.get('avg_fine', 0):,.2f}")
             with c2: st.metric("Max Fine", f"Rs. {global_metrics.get('max_fine', 0):,.2f}")
             with c3: st.metric("Min Fine", f"Rs. {global_metrics.get('min_fine', 0):,.2f}")
             with c4: st.metric("Common Payment", global_metrics.get('common_payment', 'N/A'))

        st.markdown('---')
# ==========================================================================================================
    # BEHAVIOR & ENVIRONMENTAL ANALYSIS
# ==========================================================================================================
        st.markdown("<h3 style='text-align: center;'>Behavior & Environmental Analysis</h3>", unsafe_allow_html=True)
        
        # Year Filter for Behavior Analysis
        if min_year == max_year:
             selected_years_behavior = (min_year, max_year)
        else:
             selected_years_behavior = st.slider(
                 "Filter by Year (Behavior Analysis)",
                 min_value=min_year,
                 max_value=max_year,
                 value=(min_year, max_year),
                 key="slider_behavior_year"
             )
             
        # Filter Data
        mask_behavior = (df['Date'].dt.year >= selected_years_behavior[0]) & (df['Date'].dt.year <= selected_years_behavior[1])
        df_behavior = df[mask_behavior]

        with st.expander(f"🧠 Advanced Risk Indicators ({selected_years_behavior[0]} - {selected_years_behavior[1]})", expanded=True):
             behavior_metrics = dashboard_summary.get_behavioral_analysis(df_behavior)
             
             over_speeding_count, over_speeding_pct = behavior_metrics['over_speeding_stats']
             court_count, court_pct = behavior_metrics['court_appearance_stats']
             repeat_offender_count, repeat_offender_pct = behavior_metrics['repeat_offender_stats']
             bad_weather_count, bad_weather_pct = behavior_metrics['bad_weather_stats']
             top_weather_name, top_weather_count, top_weather_pct = behavior_metrics['most_frequent_weather_stats']

             # Row 1 (3 Columns)
             col1, col2, col3 = st.columns(3)
             
             with col1:
                 st.metric(
                     label="Over-Speeding Incidents",
                     value=f"{over_speeding_count} ({over_speeding_pct:.1f}%)",
                     delta=f"{over_speeding_pct:.1f}% Rate",
                     delta_color="inner" if over_speeding_pct < 10 else "inverse",
                     help="Percentage of violations where recorded speed exceeded the limit."
                 )
             with col2:
                 st.metric(
                     label="Repeat Offenders Involved",
                     value=f"{repeat_offender_count}",
                     delta=f"Prob: {repeat_offender_pct:.1f}%",
                     delta_color="inverse",
                     help="Violations committed by drivers with more than 2 recorded offenses."
                 )
             with col3:
                 st.metric(
                     label="Court Appearance Required",
                     value=f"{court_count} ({court_pct:.1f}%)",
                     delta=f"Prob: {court_pct:.1f}%",
                     delta_color="inverse",
                     help="Percentage of violations mandating a court appearance."
                 )

             st.markdown("---")
             
             # Row 2 (3 Columns)
             col4, col5 = st.columns(2)
             
             with col4:
                 st.metric(
                     label="Most Violation Weather",
                     value=f"{top_weather_name.capitalize()}",
                     delta=f"Prob: {top_weather_pct:.1f}%",
                     delta_color="off",
                     help="Most No of Violations Observed in Weather(Fog, Rain, Snow, etc.)."
                 )
             with col5:
                  st.metric(
                     label=f"Most Frequent Weather: {top_weather_name}",
                     value=f"{top_weather_count} ({top_weather_pct:.1f}%)",
                     delta="Dominant Condition",
                     delta_color="off",
                     help=f"The weather condition under which the most violations ({top_weather_count}) occurred."
                 )
        st.markdown('---')
# ==========================================================================================================
    # Full Page Graphical Plots and Analysis
# ==========================================================================================================
        # 1. Vehicle Type vs Violation Type
        with st.container():
            st.markdown("<h3 style='text-align: center;'>Vehicle Type vs Violation Type</h3>", unsafe_allow_html=True)
            
            # Slider
            if min_year == max_year:
                 years_vehicle = (min_year, max_year)
            else:
                 years_vehicle = st.slider(
                     "Filter by Year (Vehicle Analysis)",
                     min_value=min_year, max_value=max_year, value=(min_year, max_year),
                     key="slider_vehicle_year"
                 )
            
            # Filter
            mask_vehicle = (df['Date'].dt.year >= years_vehicle[0]) & (df['Date'].dt.year <= years_vehicle[1])
            df_vehicle = df[mask_vehicle]
            
            st.pyplot(dashboard_plot.plot_vehicle_type_vs_violation_type(df_vehicle), width='stretch')
            
        st.markdown('---')
        
        # 2. Severity Heatmap
        with st.container():
            st.markdown("<h3 style='text-align: center;'>Severity Heatmap by Location</h3>", unsafe_allow_html=True)

            # Slider
            if min_year == max_year:
                 years_heatmap = (min_year, max_year)
            else:
                 years_heatmap = st.slider(
                     "Filter by Year (Heatmap Analysis)",
                     min_value=min_year, max_value=max_year, value=(min_year, max_year),
                     key="slider_heatmap_year"
                 )
            
            # Filter
            mask_heatmap = (df['Date'].dt.year >= years_heatmap[0]) & (df['Date'].dt.year <= years_heatmap[1])
            df_heatmap = df[mask_heatmap]

            st.pyplot(dashboard_plot.plot_severity_heatmap_by_location(df_heatmap), width='stretch')
        st.markdown('---')        
    # ------------------------------
    # INFO SECTION
    # ------------------------------

# Define the pages for navigation
pages = [
    st.Page("pages/00_Home_Page.py", title="Home", icon="🏠", url_path='/', default=True),

    st.Page(dashboard, title="Dashboard", icon="📊", url_path='/dashboard'),

    st.Page("pages/01_Numerical_Analysis.py", title="Numerical Analysis", icon="🔢", url_path='/numerical-analysis'),
    st.Page("pages/02_Visualize_Data.py", title="Data Visualization", icon="🎨", url_path='/data-visualization'),
    st.Page("pages/03_Trend_Analysis.py", title="Trends Analysis", icon="📈", url_path='/trends-analysis'),
    st.Page("pages/04_Map_Visualization.py", title="Map Visualization", icon="🗺️", url_path='/map-visualization'),
    

    st.Page("pages/09_Upload_Dataset.py", title="Data Management", icon="📂", url_path='/data-management'),
    st.Page("pages/10_View_Dataset.py", title="View Dataset", icon="📝", url_path='/view-dataset/'),
    st.Page("pages/11_About_Page.py", title="About", icon="ℹ️", url_path='/about'),
]

# Create the navigation in the sidebar
pg = st.navigation(pages, position='sidebar',expanded=False)
pg.run()