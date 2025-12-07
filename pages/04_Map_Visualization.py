import streamlit as st
import pandas as pd
from core.sidebar import render_sidebar
from core.utils import (
    find_location_columns,
    render_choropleth_map_on_page,
    
)
import core.map_plot as map_plot

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Map Visualization - Smart Traffic Violation Pattern Detector Dashboard", 
    page_icon="🗺️", 
    layout="wide"
)

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------



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

# ------------------------------
# Header and Subheader
# ------------------------------
st.title("🗺️ Map Visualization")
st.markdown("Visualize traffic violation data across India.")

# Ensure Date column is datetime and extract years
min_year, max_year = 2000, 2024
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if not df['Date'].isna().all():
        min_year = int(df['Date'].dt.year.min())
        max_year = int(df['Date'].dt.year.max())


# ------------------------------
# PREPARE MAP RESOURCES
# ------------------------------
geojson_data, state_prop_name = map_plot.load_geojson()
if geojson_data is None:
     st.error("Could not load GeoJSON data.")
     st.stop()
     
known_states = {feature['properties'][state_prop_name].lower() for feature in geojson_data['features']} if geojson_data else set()

# Find Location Column
valid_location_cols = find_location_columns(df, known_states)

if not valid_location_cols:
    # Fallback to categorical columns
    valid_location_cols = [col for col in df.select_dtypes(include=['object']).columns if df[col].nunique() < 50]
    if not valid_location_cols:
        st.error("No suitable location/categorical column found.")
        st.stop()

# Auto-select 'Registration_State' or 'Location' if available, else first option
default_loc_col = next((col for col in valid_location_cols if col in ['Registration_State', 'Location']), valid_location_cols[0])


# ------------------------------
# DEFAULT VISUALIZATIONS
# ------------------------------

# 1. Total Violations by Location
st.markdown("<h2 style='text-align: center; '>Total Violations by Location</h3>", unsafe_allow_html=True)

# Slider for Violations
if min_year == max_year:
    sel_years_viol = (min_year, max_year)
else:
    sel_years_viol = st.slider("Filter by Year", min_year, max_year, (min_year, max_year), key="viol_slider")

# Filter
mask_viol = (df['Date'].dt.year >= sel_years_viol[0]) & (df['Date'].dt.year <= sel_years_viol[1])
df_viol = df[mask_viol]

try:
    map_data_count = df_viol[default_loc_col].value_counts().reset_index()
    map_data_count.columns = [default_loc_col, 'Count']
    render_choropleth_map_on_page(map_data_count, geojson_data, default_loc_col, 'Count', state_prop_name, color_theme="YlOrRd", title="Violations Count")
except Exception as e:
    st.error(f"Could not generate Violations Count map: {e}")

st.markdown("---")

# 2. Total Fines by Location
st.markdown("<h2 style='text-align: center; '>Total Fines by Location</h3>", unsafe_allow_html=True)
if 'Fine_Amount' in df.columns:
    try:
        # Slider for Fines
        if min_year == max_year:
            sel_years_fines = (min_year, max_year)
        else:
            sel_years_fines = st.slider("Filter by Year", min_year, max_year, (min_year, max_year), key="fines_slider")
            
        # Filter
        mask_fines = (df['Date'].dt.year >= sel_years_fines[0]) & (df['Date'].dt.year <= sel_years_fines[1])
        df_fines = df[mask_fines]

        # Ensure numeric
        df_fines['Fine_Amount_Num'] = pd.to_numeric(df_fines['Fine_Amount'], errors='coerce').fillna(0)
        map_data_fines = df_fines.groupby(default_loc_col)['Fine_Amount_Num'].sum().reset_index()
        map_data_fines.columns = [default_loc_col, 'Total Fines']
        render_choropleth_map_on_page(map_data_fines, geojson_data, default_loc_col, 'Total Fines', state_prop_name, color_theme="PuBuGn", title="Total Fines Generated")
    except Exception as e:
         st.error(f"Could not generate Total Fines map: {e}")
else:
    st.warning("Column 'Fine_Amount' not found. Skipping Total Fines map.")

st.markdown("---")


# ------------------------------
# 3. Average Driver's Age by Location
# ------------------------------
st.markdown("<h2 style='text-align: center; '>Average Driver's Age by Location</h3>", unsafe_allow_html=True)
if 'Driver_Age' in df.columns:
    try:
        # Slider for Age
        if min_year == max_year:
            sel_years_age = (min_year, max_year)
        else:
            sel_years_age = st.slider("Filter by Year", min_year, max_year, (min_year, max_year), key="age_slider")

        # Filter
        mask_age = (df['Date'].dt.year >= sel_years_age[0]) & (df['Date'].dt.year <= sel_years_age[1])
        df_age = df[mask_age]

        # Ensure numeric
        df_age['Driver_Age'] = pd.to_numeric(df_age['Driver_Age'], errors='coerce')
        map_data_age = df_age.groupby(default_loc_col)['Driver_Age'].mean().reset_index()
        map_data_age.columns = [default_loc_col, 'Avg Age']
        render_choropleth_map_on_page(map_data_age, geojson_data, default_loc_col, 'Avg Age', state_prop_name, color_theme="OrRd", title="Average Driver's Age")
    except Exception as e:
         st.error(f"Could not generate Avg Driver's Age map: {e}")
else:
    st.warning("Column 'Driver_Age' not found. Skipping Avg Driver's Age map.")

st.markdown("---")

# ------------------------------
# CUSTOM VISUALIZATION
# ------------------------------
st.markdown("<h2 style='text-align: center; '>Custom Map Visualization</h3>", unsafe_allow_html=True)
with st.expander("Configure Custom Map", expanded=True):
    
    # Slider for Custom Map
    if min_year == max_year:
        sel_years_custom = (min_year, max_year)
    else:
        sel_years_custom = st.slider("Filter by Year", min_year, max_year, (min_year, max_year), key="custom_slider")

    c1, c2 = st.columns(2)
    with c1:
        location_col = st.selectbox("Select State Column", options=valid_location_cols, index=valid_location_cols.index(default_loc_col), key="custom_loc")

    with c2:
        # end_date input removed

        
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        # Exclude Fine_Amount_Num helper if exists
        numerical_cols = [c for c in numerical_cols if c != 'Fine_Amount_Num']
        
        value_options = ['Count of Violations'] + numerical_cols
        value_col = st.selectbox("Select Data/Value to Visualize", options=value_options, key="custom_val")

    # Controls
    cc1, cc2 = st.columns(2)
    with cc1:
        agg_func = st.selectbox("Select Aggregation", options=['Mean', 'Sum', 'Median'], disabled=(value_col == 'Count of Violations'), key="custom_agg") if value_col != 'Count of Violations' else 'Count'
    with cc2:
        color_theme = st.selectbox("Select Color Theme", ["YlGnBu", "BuPu", "GnBu", "OrRd", "PuBu", "PuBuGn", "PuRd", "RdPu", "YlGn", "YlOrBr", "YlOrRd"], index=0, key="custom_theme")

    if st.button("Generate Custom Map"):
        # Filter
        mask_custom = (df['Date'].dt.year >= sel_years_custom[0]) & (df['Date'].dt.year <= sel_years_custom[1])
        plot_df = df[mask_custom].copy()

        # Aggregate
        if value_col == 'Count of Violations':
            custom_map_data = plot_df[location_col].value_counts().reset_index()
            custom_map_data.columns = [location_col, 'Count']
            viz_val_col = 'Count'
        else:
            agg_map = {'Mean': 'mean', 'Sum': 'sum', 'Median': 'median'}
            custom_map_data = plot_df.groupby(location_col)[value_col].agg(agg_map[agg_func]).reset_index()
            viz_val_col = value_col
        
        # Store in Session State
        st.session_state.custom_map_state = {
            'map_data': custom_map_data,
            'location_col': location_col,
            'value_col': viz_val_col,
            'color_theme': color_theme,
            'title': f"Custom: {value_col} ({agg_func})"
        }

# Render from Session State if Exists
if 'custom_map_state' in st.session_state:
    state = st.session_state.custom_map_state
    render_choropleth_map_on_page(
        state['map_data'], 
        geojson_data, 
        state['location_col'], 
        state['value_col'], 
        state_prop_name, 
        state['color_theme'], 
        state['title']
    )
