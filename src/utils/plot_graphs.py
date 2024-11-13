import matplotlib.pyplot as plt
import seaborn as sns


def hist_std_config(df,column_name):
    plt.figure(figsize=(12, 6))

    plt.hist(df[column_name], bins=20, edgecolor='black', alpha=0.6, density=True)
    sns.kdeplot(data=df, x=column_name, color='blue', linewidth=2)

    plt.title(column_name + ' Distribution', fontsize=16)
    plt.xlabel(column_name, fontsize=14)
    plt.ylabel('Density', fontsize=14) 
    plt.xlim((0, 10))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show

    return plt






