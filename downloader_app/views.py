# Importing required modules
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import yt_dlp
import os

def home(request):
    return HttpResponse("Welcome to the YouTube Video Downloader!")

def youtube(request):
    if request.method == 'POST':
        try:
            # Getting link from frontend
            link = request.POST.get('link', '')
            if not link:
                return render(request, 'youtube.html', {"error": "No link provided!"})

            # Setting options for yt_dlp
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # Download the best available format with both audio and video
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Temporary server-side download path
            }

            # Downloading the video to the server
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                video_path = ydl.prepare_filename(info)  # Get the full file path
                video_title = info.get('title', 'Unknown Video')

            # Returning the video file as a download
            response = FileResponse(open(video_path, 'rb'), as_attachment=True, filename=os.path.basename(video_path))
            return response
        except yt_dlp.utils.DownloadError as e:
            # Handle errors from yt_dlp
            return render(request, 'youtube.html', {"error": f"An error occurred while downloading: {str(e)}"})
        except Exception as e:
            # Handle other exceptions
            return render(request, 'youtube.html', {"error": f"An unexpected error occurred: {str(e)}"})

    return render(request, 'youtube.html')
