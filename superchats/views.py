from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from googleapiclient.discovery import build 
from django.conf import settings 
 
API_KEY = 'AIzaSyD2sjuLmZwXdN3DdJR9WRvSIKfFCttry08' 
 
CHANNEL_ID = '' 

youtube = build('youtube', 'v3', developerKey=API_KEY) 

def get_live_video_id(channel_id): 
    request = youtube.search().list( 
        part='id', 
        channelId=channel_id, 
        eventType='live', 
        type='video'
    )  

    response = request.execute() 
    if response['items']: 
        return response['items'][0]['id']['videoId'] 
    else: 
        return None 
     
def get_superchats(video_id): 
    request = youtube.liveChatMessages().list( 
        liveChatId=video_id, 
        part='snippet,authorDetails'
    ) 
    response = request.execute() 
    return response['items'] 


@api_view(['GET']) 
def superchats_view(request): 
    video_id = get_live_video_id(CHANNEL_ID) 
    if video_id: 
        superchats_list = get_superchats(video_id) 
        data = [ 
            { 
                'author': chats['authorDetails']['displayName'], 
                'message': chats['snippet']['displayMessage'], 
                'amount': chats['snippet'].get('superChatDetails', {}).get('amountDisplayString', 'N/A')
            } 
            for chats in superchats_list
        ] 
        return Response(data) 
    else: 
        return Response({'message': 'No hay videos en directo actualmente.'}, status=404)