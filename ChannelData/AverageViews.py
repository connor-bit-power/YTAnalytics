from googleapiclient.discovery import build
import datetime
import json
import dotenv

# Your API key
API_KEY = 'AIzaSyBX34_pmV3Gp2URqbBlZIKrCVf-AhS1eBU'
CHANNEL_ID = 'UCX6OQ3DkcsbYNE6H8uQQuVA'

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_ids():
    date_today = datetime.datetime.now()
    date_last_year = date_today - datetime.timedelta(days=365)

    request = youtube.search().list(
        part='id',
        channelId=CHANNEL_ID,
        maxResults=50,
        type='video',
        publishedAfter=date_last_year.isoformat() + 'Z'
    )

    video_ids = []
    while request:
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['id']['videoId'])
        request = youtube.search().list_next(request, response)

    return video_ids

def get_views(video_ids):
    views = []
    for video_id in video_ids:
        response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        for item in response['items']:
            view_count = int(item['statistics']['viewCount'])
            views.append(view_count)

    return views

def calculate_average_views():
    video_ids = get_video_ids()
    views = get_views(video_ids)
    if views:
        return sum(views) / len(views)
    else:
        return 0

average_views = calculate_average_views()

# Output the result in JSON format
print(json.dumps({'average_views': average_views}))
