import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

# This module handles plots for the Visualization Page (02_Visualize_Data.py)

def plot_speed_exceeded_vs_weather(df):
    """
    Plots Average Speed Exceeded vs Weather Condition.
    """
    # Create new feature
    df['Speed_Exceeded'] = df['Recorded_Speed'] - df['Speed_Limit']

    fig, ax = plt.subplots(figsize=(14,7))

    # Compute mean speed exceeded and sort
    avg_speed = df.groupby('Weather_Condition')['Speed_Exceeded'].mean().sort_values(ascending=False)

    # Barplot
    sns.barplot(
        x=avg_speed.index,
        y=avg_speed.values,
        hue=avg_speed.index,
        palette='viridis',
        ax=ax
    )

    # Add value labels on bars
    for i, v in enumerate(avg_speed.values):
        ax.text(i, v + 0.5, f"{v:.1f}", ha='center', fontsize=10, fontweight='bold')

    # Titles and labels
    ax.set_title("Average Speed Exceeded vs Weather Condition", fontsize=16, fontweight='bold')
    ax.set_xlabel("Weather Condition", fontsize=14)
    ax.set_ylabel("Average Speed Exceeded (km/h)", fontsize=14)

    plt.xticks(rotation=45)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_avg_fine_by_violation_type(df):
    """
    Plots Average Fine Amount by Violation Type (Scatter Plot).
    """
    fig, ax = plt.subplots(figsize=(14,7))

    # Compute average fine amount by violation type
    avg_fines = df.groupby('Violation_Type')['Fine_Amount'].mean().sort_values(ascending=False)

    # Scatter plot
    ax.scatter(avg_fines.index, avg_fines.values, s=120, color='red')

    # Add value labels for each point
    for i, v in enumerate(avg_fines.values):
        ax.text(i, v + 5, f"{v:.0f}", ha='center', fontsize=10, fontweight='bold')

    # Titles and labels
    ax.set_title("Average Fine Amount by Violation Type (Scatter Plot)", fontsize=16, fontweight='bold')
    ax.set_xlabel("Violation Type", fontsize=14)
    ax.set_ylabel("Average Fine Amount (₹)", fontsize=14)

    plt.xticks(rotation=90)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return fig

def plot_bar_or_count(df, x_col, y_col):
    """
    Generates a bar plot or count plot based on the Y-axis selection.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if y_col == 'Count':
        # Create a count plot using seaborn
        sns.countplot(x=x_col, data=df, ax=ax, order=df[x_col].value_counts().index)
        ax.set_title(f"Count of {x_col}")
        ax.set_ylabel("Count")
    else:
        # Create a bar plot of the mean using seaborn
        sns.barplot(x=x_col, y=y_col, data=df, ax=ax, estimator=lambda x: x.mean())
        ax.set_title(f"Mean of {y_col} by {x_col}")
        ax.set_ylabel(f"Mean {y_col}")

    ax.set_xlabel(x_col)
    ax.tick_params(axis='x', rotation=45)
    fig.tight_layout()
    return fig
