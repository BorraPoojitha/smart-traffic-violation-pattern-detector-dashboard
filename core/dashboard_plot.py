import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# This module handles plots for the Dashboard (Home Page)

def plot_violation_types_distribution(df, total_no_of_violations):
    """
    Plots the distribution of violation types.
    """
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(14,6.3))
    sns.countplot(data=df,
                x='Violation_Type', 
                order=df['Violation_Type'].value_counts().iloc[::-1].index,
                hue='Violation_Type',
                palette='viridis',
                edgecolor='black', 
                linewidth=1.5
    )
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('No of Violations', fontweight='bold')
    plt.xticks(rotation=45)
    for idx, total in enumerate(df['Violation_Type'].value_counts().iloc[::-1]):
        plt.text(
            idx,
            total + (total_no_of_violations * 0.01),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black'
        )
    return plt.gcf()
# =================================================================================
def plot_fines_based_on_violation_type(summary):
    """
    Plots the fines based on violation type (Paid vs Unpaid).
    """
    # plt.style.use('dark_background') # Preserved comment from original code
    ax = summary.plot(
        kind='bar',
        stacked=True,
        figsize=(14,6.5),
        # two calm color
        color=['#FF6B6B', '#4ECDC4'],     # Paid, Unpaid
        edgecolor='black', 
        linewidth=1.5
    )
    plt.title('Fines Based on Violation Type', fontweight='bold')
    plt.xlabel('Violation Type', fontweight='bold')
    plt.ylabel('Total Fine Amount (₹)',fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)

    # 5. Format Color Bar values, Y-axis values, and add total fine above bars
    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    # Show Paid / Unpaid inside bars
    for c in ax.containers:
        ax.bar_label(c, label_type='center', fontsize=10, color='black', rotation=45)
    totals = summary.sum(axis=1)
    for idx, total in enumerate(totals):
        ax.text(
            idx,
            summary.iloc[idx].sum() + (max(totals) * 0.02),
            f'{total:,.0f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color='black'
        )
    # Legend outside plot area upper left corner
    plt.tight_layout()

    plt.legend(title="Status", bbox_to_anchor=(1, 1.05), loc="upper right", ncol=2)
    return plt.gcf()
# =================================================================================
def plot_violations_by_location(location_based_violations):
    """
    Plots a pie chart of violations by location.
    """
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(10,6.5))
    plt.pie(
        location_based_violations['No of Violations'],
        labels=location_based_violations['Location'],
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel'),
        wedgeprops={'edgecolor': 'black'}
    )
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)
    return plt.gcf()
# =================================================================================
def plot_gender_distribution(gender_distribution):
    """
    Plots the gender distribution of drivers.
    """
    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(14,6.5))
    sns.barplot(
        x=gender_distribution.index, 
        y=gender_distribution.values, 
        palette='viridis', 
        edgecolor='black', 
        linewidth=1.5)
    plt.xlabel('Gender', fontweight='bold')
    plt.ylabel('Count', fontweight='bold')
    plt.title('Gender Distribution', fontweight='bold')
    plt.xticks(rotation=25)
    plt.yticks(rotation=25)
    return plt.gcf()
# =================================================================================
