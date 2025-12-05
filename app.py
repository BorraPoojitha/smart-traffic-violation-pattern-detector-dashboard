import streamlit as st
from core import (
    dashboard_summary,
    utils,
    sidebar,
    data_variables
)

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(
    page_title="Smart Traffic Violation Dashboard",
    page_icon="🚦",
    layout="wide",
)

def home() -> None:
    # ----------------------------------------
    # HEADER SECTION
    # ----------------------------------------
    st.title("🚦 Smart Traffic Violation Summary Dashboard")

    # ----------------------------------------
    # SIDEBAR
    # ----------------------------------------
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

        # Summary Calculations for Last N Days
        no_of_days_for_summary  = st.expander("Days Filter", expanded=False).slider("Select Number of Days for Summary Calculations", min_value=7, max_value=365, value=30, step=1, key="days_slider")
        df_last_n_days = utils.get_last_n_days_data(df, no_of_days_for_summary)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"### Total Violations (Last {no_of_days_for_summary} Days)")
            summary = dashboard_summary.get_violations_summary_of_last_n_days(df_last_n_days)
            
            # Display Charts
            with st.expander("View Violation Types Distribution Chart"):
                st.write("### Violation Types Distribution")
                st.pyplot(summary.get('fig'), width='content')
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
            st.info(f"### Violations by Location (Last {no_of_days_for_summary} Days)")
            location_based_summary = dashboard_summary.get_violations_by_location(df_last_n_days)
            with st.expander("View Violations by Location Chart"):
                st.write("### Violations by Location")
                st.pyplot(location_based_summary.get('fig'), width='content',)
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
            
    # ==========================================================================================================
        with col2:
            st.info(f"### Total Fines (Last {no_of_days_for_summary} Days)")
            fine_summary = dashboard_summary.get_total_fines_generated(df_last_n_days)
            
            # Display Charts
            with st.expander("View Fines Distribution Chart"):
                st.write("### Fines Distribution")
                st.pyplot(fine_summary.get('fig'), width='content')
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
            # Average Fine per Violation
            st.info(f"### Driver's Insights (Last {no_of_days_for_summary} Days)")
            driver_insights = dashboard_summary.get_driver_insights(df_last_n_days)

            # Display Charts
            with st.expander("View Calculation Methodology"):
                st.write("### Driver Gender")
                st.pyplot(driver_insights.get('gender_fig'))
            # Metrics
            sub_col1, sub_col2= st.columns(2, border=True)
            with sub_col1:
                st.metric(label="Average Driver Age", value=f"{driver_insights.get('avg_driver_age')} years")
            with sub_col2:
                st.metric(label="Most Common Driver Gender", value=driver_insights.get('most_common_gender'))
            # with sub_col3:
            #     st.metric(label="Maximum Alcohol Level", value=f"{driver_insights.get('max_alcohol_level')}")
        st.markdown('---')     

    # ------------------------------
    # INFO SECTION
    # ------------------------------

# Define the pages for navigation
pages = [
    st.Page(home, title="Home Page", icon="🏠", default=True, url_path='/'),
    st.Page("pages/01_Numerical_Analysis.py", title="Numerical Analysis", icon="📊", url_path='/numerical-analysis'),
    st.Page("pages/02_Visualize_Data.py", title="Data Visualization", icon="🎨", url_path='/data-visualization'),
    st.Page("pages/03_Trend_Analysis.py", title="Series Trends", icon="📈", url_path='/series-trends'),
    st.Page("pages/04_Map_Visualization.py", title="Map Visualization", icon="🗺️", url_path='/map-visualization'),
    st.Page("pages/09_Upload_Dataset.py", title="Data Management", icon="📂", url_path='/data-management'),
    st.Page("pages/10_View_Dataset.py", title="View Dataset", icon="📝", url_path='/view-dataset/'),
]

# Create the navigation in the sidebar
pg = st.navigation(pages, position="sidebar")
pg.run()