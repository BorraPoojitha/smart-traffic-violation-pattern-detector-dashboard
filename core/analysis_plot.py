import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# This module handles plots for the Analysis Pages

def plot_correlation_heatmap(df, numerical_cols):
    """
    Plots a correlation heatmap for numerical columns.
    
    Parameters:
    ---
    df (pd.DataFrame): The input DataFrame.
    numerical_cols (list): List of numerical column names.
    
    Returns:
    ---
    fig (plt.Figure): A matplotlib figure object representing the correlation heatmap.
    """
    corr_matrix = df[numerical_cols].corr()

    # Plotting the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5,  fmt=".2f")
    plt.xticks(rotation=45)
    
    return plt.gcf()
