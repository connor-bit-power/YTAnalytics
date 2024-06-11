import json
import subprocess
import argparse

def run_script(script_name, arg=None):
    """ Function to run a Python script possibly with an argument. """
    command = ['python3', script_name]
    if arg:
        command.append(arg)
    subprocess.run(command)

def load_json(filename):
    """ Function to load JSON data from a file. """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist. Ensure that the necessary scripts have been run.")
        sys.exit(1)

def main(keyword):
    # Run both scripts
    run_script('search.py', keyword)
    run_script('channeldata.py')

    # Load results from both scripts
    search_results = load_json('search_results.json')
    average_views_data = load_json('average_views.json')
    average_views = average_views_data['average_views']

    # Calculate view differences and print results
    analysis_results = []
    for video in search_results:
        video_id = video['videoId']
        viewCount = int(video['viewCount'])
        difference = viewCount - average_views
        analysis_results.append({
            'videoId': video_id,
            'title': video['title'],
            'viewDifference': difference
        })

    # Output the analysis results
    print(json.dumps(analysis_results, indent=4))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze video data based on a keyword search.')
    parser.add_argument('keyword', type=str, help='The keyword to search for.')
    args = parser.parse_args()
    main(args.keyword)
