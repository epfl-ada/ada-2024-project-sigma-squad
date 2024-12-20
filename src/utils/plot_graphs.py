import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.io as pio 
import seaborn as sns
import pandas as pd
from plotly.subplots import make_subplots


def hist_std_config(df, column_name, title, nbins=50, color="#3498DB", range_x=None):
    fig = go.Figure(
        data=go.Histogram(
            x=df[column_name],
            nbinsx=nbins,
            marker=dict(color=color),
        )
    )

    fig.update_layout(
        title=title,
        xaxis=dict(title=column_name, range=range_x),
        yaxis=dict(title="Frequency"),
        
        height=400,
        width=850,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig


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
    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                text=values,
                textposition='auto',
               marker_color = ['#D9534F', '#C0392B', '#A93226', '#922B21', '#7B241C', '#641E16', '#512E2C']
            )
        ]
    )

    fig.update_layout(
        title='Fig. 1: Number of movies with required information',
        xaxis_title='',
        yaxis_title='Number of Movies',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=18, color='#FFFFFF'),
        xaxis=dict(title_font=dict(size=14, color='#FFFFFF')),
        yaxis=dict(title_font=dict(size=14, color='#FFFFFF'), gridcolor='lightgray')
    )

    pio.write_html(fig, file="plots_site/available_data.html", auto_open=False, include_plotlyjs='cdn')
    pio.write_image(fig, file="plots_site/available_data.png", format='png', scale=2)

    return fig


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


def actor_bar_plot(actor_df):
    """
    Plot the number of missing values for selected actor attributes.
    """
    
    missing_values = actor_df.isna().sum().tolist()

    
    labels = ['Date of Birth', 'Gender', 'Height', 'Ethnicity', 'Age at First Movie Release']
    values = missing_values[:len(labels)]  # Select only the relevant attributes

    fig = go.Figure(
        data=go.Bar(
            x=labels,
            y=values,
            text=values,
            textposition='auto',
            marker=dict(
                color=['#FAD0C9', '#F8A5B1', '#FDCB82', '#E17055', '#D35400']
            )
        )
    )

    fig.update_layout(
        title="Missing Values per Attribute",
        xaxis=dict(title="Attributes"),
        yaxis=dict(title="Number of Missing Values"),
        
        height=400,
        width=850,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=False
    )

    return fig



def actor_index_distribution(actor_df):
    """
    Plot the Actor Score Index distribution for all actors and actors with known heights using Plotly.
    """
    
    filtered_actor = actor_df.dropna(subset=['Actor height'])

    # Calculate mean and standard deviation for both datasets
    stats = {
        'Dataset': ['All Actors', 'Actors with Known Heights'],
        'Mean': [actor_df['Actor Score Index'].mean(), filtered_actor['Actor Score Index'].mean()],
        'Standard Deviation': [actor_df['Actor Score Index'].std(), filtered_actor['Actor Score Index'].std()]
    }
    stats_df = pd.DataFrame(stats).set_index('Dataset')

  
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("All Actors", "Actors with Known Heights"),
        shared_yaxes=True
    )

   
    fig.add_trace(
        go.Histogram(
            x=actor_df['Actor Score Index'],
            nbinsx=50,
            name='All Actors',
            marker=dict(color='blue', opacity=0.7)
        ),
        row=1, col=1
    )


    fig.add_trace(
        go.Histogram(
            x=filtered_actor['Actor Score Index'],
            nbinsx=50,
            name='Actors with Known Heights',
            marker=dict(color='green', opacity=0.7)
        ),
        row=1, col=2
    )


    fig.update_layout(
        title="Actor Score Index Distribution",
        xaxis=dict(title="Actor Score Index", range=[0, 10]),
        xaxis2=dict(title="Actor Score Index", range=[0, 10]),
        yaxis=dict(title="Frequency"),
        
        height=400,
        width=900,
        margin=dict(l=50, r=50, t=80, b=50),
        showlegend=False
    )
    fig.show()
    return stats_df



def plot_ethnicity_distribution(df, ethnicity_column='Ethnicity'):

    ethnicity_counts = df[ethnicity_column].value_counts()

    # Set the color palette
    color_palette = sns.color_palette("muted")

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=ethnicity_counts.index, y=ethnicity_counts.values, palette=color_palette)

    # Set the title and labels
    plt.title('Ethnicity Distribution', fontsize=18, weight='bold')
    plt.xlabel('Ethnicity', fontsize=16)
    plt.ylabel('Count', fontsize=16)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Show the plot
    plt.tight_layout()
    plt.show()


def profitability_histograms(data, revenue_budget_max=200, log_revenue_budget_max=13, 
                                     output_image_path="plots_site/responsive_histograms.png", 
                                     output_html_path="plots_site/responsive_graph.html"):
    """
    Create histograms for Profitability and Log Profitability distributions.

    Parameters:
        data (DataFrame): Input data containing 'Profitability' and 'Log Profitability' columns.
        revenue_budget_max (int, optional): Maximum value for filtering 'Profitability'. Defaults to 200.
        log_revenue_budget_max (int, optional): Maximum value for filtering 'Log Profitability'. Defaults to 13.
        output_image_path (str, optional): Path to save the resulting PNG image. Defaults to 'plots_site/responsive_histograms.png'.
        output_html_path (str, optional): Path to save the resulting HTML file. Defaults to 'plots_site/responsive_graph.html'.

    Returns:
        None
    """

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.3,
        subplot_titles=(
            "Profitability Distribution", 
            "Log Profitability Distribution"
        )
    )

    fig.add_trace(
        go.Histogram(
            x=data['Profitability'][data['Profitability'] <= revenue_budget_max],
            nbinsx=200,
            name='Profitability',
            marker=dict(color='orange', opacity=0.7)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=data['Log Profitability'][data['Log Profitability'] <= log_revenue_budget_max],
            nbinsx=50,
            name='Log Profitability',
            marker=dict(color='darkorange', opacity=0.7)
        ),
        row=2, col=1
    )

    fig.update_layout(
        title="Distribution of Profitability and Log Profitability",
        xaxis=dict(title="Profitability [-]"),
        xaxis2=dict(title="Log Profitability [-]"),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title="Frequency"),
        height=400,  # Adjust height to a smaller value
        width=850,   # Adjust width for better scaling
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )



    pio.write_image(fig, file=output_image_path, format='png', scale=2)
    pio.write_html(fig, file=output_html_path, auto_open=False, include_plotlyjs='cdn')
    return fig



def movie_revenue_distribution_plot(data, revenue_max=500_000_000, log_revenue_max=13,
                                           html_output_path="plots_site/movie_revenue_distribution.html",
                                           png_output_path="plots_site/movie_revenue_distribution.png"):
    """
    Create histograms for Movie Box Office Revenue and Log Revenue distributions.

    Parameters:
        data (DataFrame): Input data containing 'Movie box office revenue' and 'Log Revenue' columns.
        revenue_max (int, optional): Maximum threshold for 'Movie box office revenue'. Defaults to 500,000,000.
        log_revenue_max (int, optional): Maximum threshold for 'Log Revenue'. Defaults to 13.
        html_output_path (str, optional): Path to save the HTML file. Defaults to 'plots_site/movie_revenue_distribution.html'.
        png_output_path (str, optional): Path to save the PNG image. Defaults to 'plots_site/movie_revenue_distribution.png'.

    Returns:
        None
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.3,
        subplot_titles=(
            "Movie Box Office Revenue Distribution", 
            "Log Movie Box Office Revenue Distribution"
        )
    )

    # Add the Movie Box Office Revenue histogram
    fig.add_trace(
        go.Histogram(
            x=data['Movie box office revenue'][data['Movie box office revenue'] <= revenue_max],
            nbinsx=100,
            name='Movie box office revenue',
            marker=dict(color='gray', opacity=0.7)
        ),
        row=1, col=1
    )

    # Add the Log Movie Box Office Revenue histogram
    fig.add_trace(
        go.Histogram(
            x=data['Log Revenue'][data['Log Revenue'] <= log_revenue_max],
            nbinsx=50,
            name='Log Revenue',
            marker=dict(color='black', opacity=0.7)
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title="Distribution of Box Office Revenue and Log Revenue",
        xaxis=dict(title="Box Office Revenue [USD (millions)]"),
        xaxis2=dict(title="Log Revenue [-]"),
        yaxis=dict(title="Frequency"),
        yaxis2=dict(title="Frequency"),
        height=400,  # Adjust height to a smaller value
        width=850,   # Adjust width for better scaling
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Show the figure


    # Save the figure as an image and an HTML file
    pio.write_html(fig, file=html_output_path, auto_open=False, include_plotlyjs='cdn')
    pio.write_image(fig, file=png_output_path, format='png', scale=2)
    return fig 

def movie_score_distribution_plot(data, score_max=10, 
                                         html_output_path="plots_site/movie_score_distribution.html", 
                                         png_output_path="plots_site/movie_score_distribution.png"):
    """
    Create a histogram for the distribution of movie scores.

    Parameters:
        data (DataFrame): Input data containing the 'Movie score' column.
        score_max (int, optional): Maximum threshold for movie scores. Defaults to 10.
        html_output_path (str, optional): Path to save the HTML file. Defaults to 'plots_site/movie_score_distribution.html'.
        png_output_path (str, optional): Path to save the PNG image. Defaults to 'plots_site/movie_score_distribution.png'.

    Returns:
        None
    """
    # Check for the 'Movie score' column
    if 'Movie Success Index' not in data.columns:
        raise ValueError("Dataset must contain a 'Movie score' column.")

    # Drop NaN values and filter invalid data
    filtered_scores = data['Movie Success Index'].dropna()
    filtered_scores = filtered_scores[filtered_scores <= score_max]

    # Create the histogram
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=filtered_scores,
            nbinsx=100,  # Number of bins
            name='Movie Success Index',
            marker=dict(color='teal', opacity=0.7)
        )
    )

    # Update layout
    fig.update_layout(
        title="Distribution of Movie Scores",
        xaxis=dict(title="Movie Score [-]",range=[0, 10]  ),
        yaxis=dict(title="Frequency"),
        height=300,
        width=850,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Show the figure


    # Save the figure as an HTML file and an image
    pio.write_html(fig, file=html_output_path, auto_open=False, include_plotlyjs='cdn')
    pio.write_image(fig, file=png_output_path, format='png', scale=2)
    
    return fig 



def plot_movie_review_distribution(df):
    fig = go.Figure(
        data=go.Histogram(
            x=df['Review score'],
            nbinsx=100,  
            marker=dict(color="#B22222", opacity=0.75), 
        )
    )

    fig.update_layout(
        title="Distribution of movies reviews",
        xaxis=dict(title="Movie reviews"),
        yaxis=dict(title="Frequency"),
        height=400,  # Adjust height to a smaller value
        width=850,   # Adjust width for better scaling
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.write_html('plots_site/movie_reviews_distribution.html')
    return fig