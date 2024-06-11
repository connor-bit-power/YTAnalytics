from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

# Your API key and channel ID
API_KEY = 'AIzaSyBX34_pmV3Gp2URqbBlZIKrCVf-AhS1eBU'
CHANNEL_ID = 'UCX6OQ3DkcsbYNE6H8uQQuVA'

def get_youtube_service():
    """Builds and returns the YouTube service object."""
    return build('youtube', 'v3', developerKey=API_KEY)

def get_recent_videos():
    youtube = get_youtube_service()
    date_three_months_ago = datetime.now() - timedelta(days=90)
    date_three_months_ago_iso = date_three_months_ago.isoformat() + "Z"  # Format for YouTube API

    request = youtube.search().list(
        part="id",
        channelId=CHANNEL_ID,
        maxResults=50,
        type="video",
        publishedAfter=date_three_months_ago_iso
    )
    
    videos = []
    while request:
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response['items']]
        videos += get_video_details(video_ids)
        request = youtube.search().list_next(request, response)

    return videos

def get_video_details(video_ids):
    youtube = get_youtube_service()
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()

    video_details = []
    for item in response['items']:
        # Retrieve the URL of the highest resolution thumbnail available
        thumbnails = item['snippet']['thumbnails']
        maxres_thumbnail_url = thumbnails.get('maxres', {}).get('url')
        if not maxres_thumbnail_url:  # Fallback to high resolution if maxres is unavailable
            maxres_thumbnail_url = thumbnails.get('high', {}).get('url')

        video_details.append({
            "id": item['id'],
            "title": item['snippet']['title'],
            "publishedAt": item['snippet']['publishedAt'],
            "thumbnailUrl": maxres_thumbnail_url,  # Include the thumbnail URL
            "viewCount": item['statistics'].get('viewCount', '0'),
            "likeCount": item['statistics'].get('likeCount', '0'),
            "commentCount": item['statistics'].get('commentCount', '0')
        })
    
    return video_details

if __name__ == "__main__":
    videos = get_recent_videos()
    print(json.dumps(videos, indent=4))
