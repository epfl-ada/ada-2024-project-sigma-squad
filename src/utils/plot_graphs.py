import matplotlib.pyplot as plt
import seaborn as sns

def hist_std_config(df, column_name):
    '''Easy plotting of different histograms with KDE for different columns of a DataFrame'''
    
    color_palette = ['#FAD0C9', '#F8A5B1', '#FDCB82', '#E17055', '#D35400', '#F39C12', '#F1C40F']
    
    sns.set_palette("muted")  
    plt.figure(figsize=(12, 6))
    
    plt.hist(df[column_name], bins=20, edgecolor='gray', alpha=0.6, density=True, color=color_palette[2])
    sns.kdeplot(data=df, x=column_name, color=color_palette[4], linewidth=2.5)
    
    plt.title(f'{column_name} Distribution', fontsize=18, weight='bold')
    plt.xlabel(column_name, fontsize=16)
    plt.ylabel('Density', fontsize=16)
    
    if column_name == 'Profitability score':

        break_even_point = 10 * (0 - df['Log Profitability'].min()) / (df['Log Profitability'].max() - df['Log Profitability'].min())
       
        
        plt.axvline(x=break_even_point, color='red', linestyle='--', label='Break-even Point')
        plt.legend()
        
    if column_name == 'Nomination multiplier':
        plt.xlim((1, 1.3))
        plt.ylim((0, 4))
    else:
        plt.xlim((0, 10))
    
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()
    return



def hist_std_config_ax(df, column_name, ax):
    '''Easy plotting of different histograms with KDE for different columns of a DataFrame'''
    color_palette = ['#FAD0C9', '#F8A5B1', '#FDCB82', '#E17055', '#D35400', '#F39C12', '#F1C40F']
    
    sns.set_palette("muted")
    
    ax.hist(df[column_name], bins=20, edgecolor='gray', alpha=0.6, density=True, color=color_palette[2])
    sns.kdeplot(data=df, x=column_name, color=color_palette[4], linewidth=2.5, ax=ax)
    
    ax.set_title(f'{column_name} Distribution', fontsize=18, weight='bold')
    ax.set_xlabel(column_name, fontsize=16)
    ax.set_ylabel('Density', fontsize=16)

    if column_name == 'Profitability score':
        break_even_point = 10 * (0 - df['Log Profitability'].min()) / (df['Log Profitability'].max() - df['Log Profitability'].min())
        ax.axvline(x=break_even_point, color='red', linestyle='--', label='Break-even Point')
        ax.legend()

    if column_name == 'Nomination multiplier':
        ax.set_xlim((1, 1.3))
        ax.set_ylim((0, 4))
    else:
        ax.set_xlim((0, 10))
    
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    return


def bar_plot_available_data(df): 
    n_revenue = int(df['Movie box office revenue'].count())
    n_budget = int(df['Movie budget'].count())
    n_votes = int(df['Movie votes'].count())
    n_score = int(df['Review score'].count())
    n_nomination = int(df['Number of nomination'].count())

    n_all_info = int(df.dropna(subset=['Movie box office revenue', 'Movie budget', 'Movie votes', 'Review score', 'Number of nomination']).shape[0])
    n_no_nomin = int(df.dropna(subset=['Movie box office revenue', 'Movie budget', 'Movie votes', 'Review score']).shape[0])

    labels = ['Revenue', 'Budget', 'Votes', 'Score', 'Nominations', 'All except nominations', 'All info']
    values = [n_revenue, n_budget, n_votes, n_score, n_nomination, n_no_nomin, n_all_info]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, values, color=['#FAD0C9', '#F8A5B1', '#FDCB82', '#E17055', '#D35400', '#F39C12', '#F1C40F'])

    plt.title('Number of movies with required information', fontsize=18, fontweight='normal', color='#333333')  # Indigo color
    plt.ylabel('Number of Movies', fontsize=14, color='#333333')  # Dark gray for axis label
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, int(yval), ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.show
    return


def top5_best(df): 
    return df.sort_values(by='Movie Success Index', ascending=False).head(5)[['Movie name','Movie release date', 'Movie Success Index', 'Review score', 'Revenue score', 'Profitability score']]


def top5_worst(df): 
    return df.sort_values(by='Movie Success Index', ascending=True).head(5)[['Movie name','Movie release date', 'Movie Success Index', 'Review score', 'Revenue score', 'Profitability score']]


def oscar_pie_chart(df):
    color_palette = ['#FAD0C9', '#F8A5B1', '#FDCB82', '#E17055', '#D35400', '#F39C12', '#F1C40F', 
                     '#FAB1A0', '#FF7675', '#FDCB6E', '#E74C3C', '#D98880', '#E59866', '#FFC300']

    nomination_count = df['Number of nomination'].astype(int).value_counts()

    # Calculate values for the first pie chart
    no_nomination_count = nomination_count.get(0, 0)
    has_nomination_count = nomination_count.sum() - no_nomination_count

    # Data for the first pie chart
    first_pie_labels = ['No Oscar Nomination', '> 1 Oscar Nomination']
    first_pie_sizes = [no_nomination_count, has_nomination_count]

    # Plot the first pie chart
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.pie(first_pie_sizes, labels=first_pie_labels, autopct='%1.1f%%', startangle=0, colors=[color_palette[2],color_palette[4]])
    plt.title('Percentage of Movies With vs. Without Oscar Nominations')

    # Data for the second pie chart
    nominated_movies_count = nomination_count[nomination_count.index != 0]

    # Plot the second pie chart
    plt.subplot(1, 2, 2)
    nominated_movies_count.plot(kind='pie', autopct='%1.1f%%', startangle=0, colors=color_palette, legend=None, labels=['']*len(nominated_movies_count), pctdistance=1.2)
    plt.title('Distribution of Oscar Nominations (for Movies with Nominations)')
    plt.ylabel('')
    plt.gca().set_ylabel('')
    plt.gca().legend(labels=(nomination_count.index + 1).tolist(), loc="center left", bbox_to_anchor=(1.1, 0.5), title="Number of Nominations")

    plt.tight_layout()
    plt.show()
    return