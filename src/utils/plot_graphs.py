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
    

    if column_name == 'Nomination multiplier':
        plt.xlim((1, 1.3))
        plt.ylim((0, 4))
    else:
        plt.xlim((0, 10))
    
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()
    
    return plt


def bar_plot_available_data(df): 
    n_revenue = int(df['Movie box office revenue'].count())
    n_budget = int(df['Movie budget'].count())
    n_votes = int(df['Movie votes'].count())
    n_score = int(df['Movie score'].count())
    n_nomination = int(df['Number of nomination'].count())

    n_all_info = int(df.dropna(subset=['Movie box office revenue', 'Movie budget', 'Movie votes', 'Movie score', 'Number of nomination']).shape[0])
    n_no_nomin = int(df.dropna(subset=['Movie box office revenue', 'Movie budget', 'Movie votes', 'Movie score']).shape[0])

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

    