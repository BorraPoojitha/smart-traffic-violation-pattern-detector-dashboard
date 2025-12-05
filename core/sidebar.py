import streamlit as st
import pandas as pd
import os
from datetime import datetime

def render_sidebar() -> pd.DataFrame:
    """
    Renders the sidebar components including the dataset selector.
    Returns the selected and loaded pandas DataFrame.
    """
    st.sidebar.header("Dataset Selector")
    
    # Get the list of available datasets
    dataset_folder = "dataset"
    uploaded_dataset_folder = "uploaded_datasets"
    related_uploads_folder = "related_uploads"
    generated_dataset_folder = "generated_fake_traffic_datasets"
    other_party_uploads_folder = "other_party_uploads"
    
    dataset_options = {}

    # Add datasets from the 'dataset' folder
    if os.path.exists(dataset_folder):
        for filename in os.listdir(dataset_folder):
            if filename.endswith(".csv"):
                dataset_options[f"{filename} [Sample]"] = os.path.join(dataset_folder, filename)

    # Function to scan a directory and add to options
    def scan_and_add_datasets(directory, prefix):
        if os.path.exists(directory):
            # Scan for date-based directories (for generated data)
            if "generated" in directory:
                for date_dir in sorted(os.listdir(directory), reverse=True):
                    full_date_dir = os.path.join(directory, date_dir)
                    if os.path.isdir(full_date_dir):
                        for file_name in sorted(os.listdir(full_date_dir)):
                            if file_name.endswith('.csv'):
                                display_name = f"{file_name} [{prefix} - {date_dir}]"
                                dataset_options[display_name] = os.path.join(full_date_dir, file_name)
            else: # Original logic for other directories
                for file_name in sorted(os.listdir(directory)):
                    if file_name.endswith('.csv'):
                        dataset_options[f"{file_name} [{prefix}]"] = os.path.join(directory, file_name)

    # Scan new directories in the desired order
    scan_and_add_datasets(generated_dataset_folder, "Fake Generated")
    scan_and_add_datasets(related_uploads_folder, "Legacy")
    scan_and_add_datasets(other_party_uploads_folder, "Other CSVs")

    # Add datasets from the 'uploaded_datasets' folder (legacy)
    if os.path.exists(uploaded_dataset_folder):
        for root, dirs, files in os.walk(uploaded_dataset_folder):
            for filename in files:
                if filename.endswith(".csv"):
                    # Get the parent directory name for context
                    parent_dir = os.path.basename(root)
                    dataset_options[f"[Legacy] {parent_dir}/{filename}"] = os.path.join(root, filename)

    # Display the selectbox in the sidebar
    selected_dataset_display_name = st.sidebar.selectbox(
        "Choose a dataset", list(dataset_options.keys())
    )
    
    if not selected_dataset_display_name:
        st.sidebar.warning("Please select a dataset.")
        return None

    selected_dataset_path = dataset_options[selected_dataset_display_name]

    # Load the selected dataset
    @st.cache_data
    def load_data(path):
        df = pd.read_csv(path)
        return df.copy() # Return a copy to prevent mutation of cached data

    df = load_data(selected_dataset_path)
    
    st.sidebar.success(f"Loaded dataset: **{selected_dataset_display_name}**")
    
    return df.copy()
