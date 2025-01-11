import yt_dlp
from config import MAX_RESULTS, DOWNLOAD_PATH

async def search_youtube(query: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch{MAX_RESULTS}:{query}", download=False)['entries']
            return [{'id': video['id'], 'title': video['title']} for video in results]
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []

async def download_youtube(video_id: str, type_: str, quality: str):
    file_path = f"{DOWNLOAD_PATH}{video_id}"
    
    if type_ == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{file_path}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
        }
        file_path += '.mp3'
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': f'{file_path}.%(ext)s',
        }
        file_path += '.mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    
    return file_path
