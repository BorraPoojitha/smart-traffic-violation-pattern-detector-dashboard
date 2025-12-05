import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# This module handles plots for Trend Analysis

def plot_trend_analysis_line(attribute_based_pivot, x_axis_label, line_category_label):
    """
    Generates a trend line plot.
    
    Parameters:
    - attribute_based_pivot: DataFrame containing the pivoted data for plotting.
    - x_axis_label: Label for the X-axis.
    - line_category_label: Label for the line category (legend).
    
    Returns:
    - fig: The matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    markers = ['o', '*', 'x', 's', 'p', 'd', 'h', 'D', 'H']
    # Dark Background style
    sns.set_style("darkgrid")

    for i, col in enumerate(attribute_based_pivot.columns):
        ax.plot(attribute_based_pivot.index, attribute_based_pivot[col], marker=markers[i % len(markers)], linestyle='-', linewidth=2, label=col)

    ax.set_title(f"{line_category_label.replace('_',' ').title()} Trend based on {x_axis_label.replace('_',' ').title()}", fontsize=14)
    ax.set_xlabel(x_axis_label.replace(" ", " ").title(), fontsize=12)
    ax.set_ylabel("Number of Violations", fontsize=12)
    
    plt.xticks(rotation=45, ha="right", fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax.legend(title=line_category_label.replace("_"," ").title(), bbox_to_anchor=(1.02, 1), loc='upper left')
    
    fig.tight_layout()
    return fig

def plot_categorical_heatmap(percent_pivot, annot, x_label, y_label):
    """
    Generates a categorical heatmap.
    
    Parameters:
    - percent_pivot: DataFrame containing percentage values.
    - annot: DataFrame or array containing annotation strings.
    - x_label: Label for the X-axis.
    - y_label: Label for the Y-axis.
    
    Returns:
    - fig: The matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.heatmap(
        percent_pivot,
        annot=annot,
        fmt="",
        cmap="coolwarm",
        linewidths=0.5,
        vmin=0,
        vmax=100,
        ax=ax
    )
    
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_label, fontsize=16)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig
