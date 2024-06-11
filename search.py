import sys
import os
import re
import json
import captions
import argparse

def main():
    parser = argparse.ArgumentParser(description='Search captions for a specific word and return JSON with counts, stats, and publication dates per video.')
    parser.add_argument('word', type=str, help='The word to search for in the captions.')
    args = parser.parse_args()

    p = captions.Parser()
    p.parse('mrbeast')

    results = {}
    word_refs = p.findWord(args.word.lower()) 

    for ref in word_refs:
        video_id = ref.videoId
        if video_id not in results:
            results[video_id] = {
                'videoId': video_id,
                'title': ref.title.decode('utf-8'),
                'publishedAt': ref.publishedAt,  
                'count': 0,
                'viewCount': ref.stats['viewCount'],
                'likeCount': ref.stats['likeCount'] 
            }
        results[video_id]['count'] += 1

    json_output = list(results.values())
    
    print(json.dumps(json_output, indent=4))
    
if __name__ == '__main__':
    main()
