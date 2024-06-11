import json
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import argparse

def run_search_script(keyword):
    """ Runs the search script to generate the necessary JSON data file. """
    subprocess.run(['python3', 'search.py', keyword])

def load_data(filename):
    """ Load JSON data from a file into a pandas DataFrame. """
    with open(filename, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def plot_data(df):
    """ Plot the data using a line graph for viewCount on a numerically descending y-axis and a bar graph for count. """
    # Convert 'viewCount' from string to integer
    df['viewCount'] = df['viewCount'].astype(int)

    # Sort the dataframe by 'count' in descending order
    df = df.sort_values('count', ascending=False)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Creating a bar graph for the 'count' on the primary y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Videos (Title)')
    ax1.set_ylabel('Count of Mentions', color=color)
    bars = ax1.bar(df['title'], df['count'], color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticklabels(df['title'], rotation=45, ha="right")

    # Creating a line graph for the 'viewCount' on the secondary y-axis
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('ViewCount', color=color)  # we already handled the x-label with ax1
    line = ax2.plot(df['title'], df['viewCount'], color=color, marker='o', linestyle='-', linewidth=2)
    max_view_count = df['viewCount'].max()
    buffer = max_view_count * 0.20  # Adding 20% buffer
    ax2.set_ylim(0, max_view_count + buffer)  # Manually setting the limits of the right y-axis
    ax2.tick_params(axis='y', labelcolor=color)

    # Title and legend
    plt.title('Video Mentions and ViewCounts')
    fig.tight_layout()  # to ensure the layout is not too cramped

    # Legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Show plot
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot video data based on a keyword search.')
    parser.add_argument('keyword', type=str, help='The keyword to search for and plot data.')
    args = parser.parse_args()

    # Run search.py to generate the required data
    run_search_script(args.keyword)

    # Load and plot data
    df = load_data('search_results.json')
    plot_data(df)
