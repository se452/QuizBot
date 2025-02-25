import os
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(youtube_url):
    """
    Extract video ID from YouTube URL.
    
    Args:
        youtube_url (str): The URL of the YouTube video
        
    Returns:
        str: YouTube video ID
    """
    # Handle different URL formats
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path.startswith(('/embed/', '/v/')):
            return parsed_url.path.split('/')[2]
    raise ValueError("Invalid YouTube URL")

def download_youtube_audio(youtube_url):
    """
    Get transcript from a YouTube video.
    
    Args:
        youtube_url (str): The URL of the YouTube video
        
    Returns:
        str: Video transcript
    """
    try:
        # Extract video ID from URL
        video_id = get_video_id(youtube_url)
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript text
        transcript = ' '.join([entry['text'] for entry in transcript_list])
        
        return transcript
            
    except Exception as e:
        raise Exception(f"Error getting YouTube transcript: {str(e)}") 