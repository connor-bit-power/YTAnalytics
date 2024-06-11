import strawberry
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from isodate import parse_duration
import os
from dotenv import load_dotenv
load_dotenv() 


API_KEY = os.getenv('YOUTUBE_API_KEY')
assert API_KEY is not None, "YOUTUBE_API_KEY environment variable not set."

def get_youtube_service():
    """Builds and returns the YouTube service object."""
    return build('youtube', 'v3', developerKey=API_KEY)

@strawberry.type
class Video:
    id: str
    title: str
    publishedAt: str
    thumbnailUrl: str
    viewCount: int
    likeCount: int
    commentCount: int

@strawberry.type
class Query:
    @strawberry.field
    def get_recent_videos(self, channel_id: str) -> list[Video]:
        youtube = get_youtube_service()
        date_three_months_ago = datetime.now() - timedelta(days=90)
        date_three_months_ago_iso = date_three_months_ago.isoformat() + "Z"

        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            type="video",
            publishedAfter=date_three_months_ago_iso
        )
        
        videos = []
        while request:
            response = request.execute()
            video_ids = [item['id']['videoId'] for item in response['items']]
            videos += get_video_details(youtube, video_ids)
            request = youtube.search().list_next(request, response)

        return videos

def get_video_details(youtube, video_ids):
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()

    video_details = []
    for item in response['items']:
        duration = parse_duration(item['contentDetails']['duration']).total_seconds()
        if duration > 60:  # Filtering out videos shorter than 60 seconds
            thumbnails = item['snippet']['thumbnails']
            maxres_thumbnail_url = thumbnails.get('maxres', {}).get('url')
            if not maxres_thumbnail_url:  # Fallback to high resolution if maxres is unavailable
                maxres_thumbnail_url = thumbnails.get('high', {}).get('url')

            video_details.append(Video(
                id=item['id'],
                title=item['snippet']['title'],
                publishedAt=item['snippet']['publishedAt'],
                thumbnailUrl=maxres_thumbnail_url,
                viewCount=int(item['statistics'].get('viewCount', '0')),
                likeCount=int(item['statistics'].get('likeCount', '0')),
                commentCount=int(item['statistics'].get('commentCount', '0'))
            ))

    return video_details

# Create a Strawberry GraphQL schema
schema = strawberry.Schema(query=Query)

# Import FastAPI and create an instance
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app = FastAPI()

# Create a GraphQL router and mount it
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
