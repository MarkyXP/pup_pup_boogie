import yt_dlp
import urllib.request
import os

def download_audio(url):
    audio_opts = {
        'extract_audio': True,      # Extract audio
        'format': 'bestaudio',
        'outtmpl': 'audio/%(title)s|%(duration)s/audio.%(ext)s', # Output file name template
        'noplaylist': True,         # Only download single video
        'progress_hooks': [my_progress_hook],
        'force_ipv4': True
    }
    print("\nStarting audio download...")
    with yt_dlp.YoutubeDL(audio_opts) as ydl:
        # Extract the metadata of the video
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'N/A')
        video_duration = info_dict.get('duration', 'N/A') # Duration in seconds
        # Thumbnails are typically a list, we can get the URL of the last (highest quality) one
        video_thumbnail_url = info_dict.get('thumbnails', [{}])[-1].get('url', 'N/A')
        thumbnail_format = video_thumbnail_url.split('.')[-1]  # Get the file extension
        output_folderpath = f"audio/{video_title}|{video_duration}"
        # Save the thumbnail
        os.makedirs(output_folderpath, exist_ok=True)
        urllib.request.urlretrieve(
            video_thumbnail_url,
            f"{output_folderpath}/thumbnail.{thumbnail_format}"
        )
        # Save the audio file
        ydl.download(url)
    print("Audio download complete.")

# Optional: A simple progress hook function
def my_progress_hook(d):
    if d['status'] == 'finished':
        print(f"Done downloading {d['filename']}")

# Run the functions
if __name__ == "__main__":
    video_url = "https://youtube.com/watch?v=puiZFmde8kE"
    video_url = "https://youtube.com/watch?v=cJuO985zF8E"
    video_url = "https://youtube.com/watch?v=bGCBbYebP0s" # Please Please Please
    video_url = "https://youtube.com/watch?v=k-cUlvsMXaE" # Pink Monky Club
    video_url = "https://youtube.com/watch?v=puiZFmde8kE"
    #get_video_info(video_url)
    download_audio(video_url)
