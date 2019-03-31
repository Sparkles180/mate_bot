from googleapiclient.discovery import build
from mate_config import config


def search(query):
    youtube = build('youtube', 'v3', developerKey=config.get('api_key'))
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query,
        type="video"
    )
    response = request.execute()
    return "https://www.youtube.com/watch?v={}".format(response['items'][0]['id']['videoId'])
