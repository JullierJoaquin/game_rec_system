import seaborn as sns
import matplotlib.pyplot as plt

# Color palete
back_color = "#0D1117" # github background color
main_color = "#FFFFFF" # white

sns.set_theme(style="whitegrid")

# 
def missing_values_heatmap(dataframe, title):
    # Create and configurate heatmap
    sns.heatmap(data=dataframe.isnull().T, cbar=False, annot_kws={"color": "red"}, cmap=sns.color_palette([main_color, back_color]))
    plt.gcf().set_facecolor("#0D1117") # Background
    plt.title(f"{title} missing values", fontsize=10, loc='left', color=main_color) # Title
    plt.yticks(fontsize=9, color=main_color) # Y axis
    plt.xticks([]) # X axis
    # Save and show
    plt.savefig(f"gallery/{title}.png", format='png', dpi=300, bbox_inches='tight')
    plt.show()

#
def histogram(column, title):
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.gcf().set_facecolor("#0D1117") # Background
    plt.gca().set_facecolor("#0D1117") # Background
    plt.hist(column, bins=len(column.value_counts()), color=main_color, edgecolor=back_color)
    # Title
    plt.title(title, fontsize=10, loc='right', color=main_color)
    # X axis
    plt.xticks(fontsize=9, color=main_color) 
    plt.xlabel('')
    # Y axis
    plt.yticks(fontsize=9, color=main_color)
    plt.ylabel('')
    # Grid
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(color='darkgrey', linewidth=0.25)
    # Annotate the bars with their respective counts
    #for p in ax.patches:
    #    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), 
    #                ha='center', va='center', rotation=90, fontsize=9, color=back_color, xytext=(0, -20), textcoords='offset points')
    # Muestra el histograma
    plt.savefig(f"gallery/{title}.png", format='png', dpi=300, bbox_inches='tight')
    plt.show()

#
def barplot(data, title):
    plt.figure(figsize=(10, 6))
    plt.gcf().set_facecolor("#0D1117") # Background
    plt.gca().set_facecolor("#0D1117") # Background
    data.plot(kind='bar', color=main_color, edgecolor=back_color)
    # Title
    plt.title(title, fontsize=10, loc='right', color=main_color)
    # X axis
    plt.xticks(fontsize=9, color=main_color) 
    plt.xlabel('')
    # Y axis
    plt.yticks(fontsize=9, color=main_color)
    plt.ylabel('')
    # Grid
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.grid(color='darkgrey', linewidth=0.25)
    # Annotate the bars with their respective counts
    #for p in ax.patches:
    #    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), 
    #                ha='center', va='center', rotation=90, fontsize=9, color=back_color, xytext=(0, -20), textcoords='offset points')
    # Muestra el histograma
    plt.savefig(f"gallery/{title}.png", format='png', dpi=300, bbox_inches='tight')
    plt.show()
    