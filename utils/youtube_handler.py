import yt_dlp
from config import MAX_RESULTS, DOWNLOAD_PATH

async def search_youtube(query: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        # Add these options to handle the verification issue
        'cookiesfrombrowser': ('chrome',),  # Use cookies from Chrome
        'nocheckcertificate': True,
        'ignoreerrors': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch{MAX_RESULTS}:{query}", download=False)['entries']
            return [{'id': video['id'], 'title': video['title']} for video in results if video]
        except Exception as e:
            print(f"Error searching YouTube: {e}")
            return []

async def download_youtube(video_id: str, type_: str, quality: str):
    file_path = f"{DOWNLOAD_PATH}{video_id}"
    
    common_opts = {
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('chrome',),  # Use cookies from Chrome
        'geo_bypass': True,
    }
    
    if type_ == "audio":
        ydl_opts = {
            **common_opts,
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
            **common_opts,
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': f'{file_path}.%(ext)s',
        }
        file_path += '.mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
        return file_path
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
