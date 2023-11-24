# yt-dlp の依存関係の追加が必要
from yt_dlp import YoutubeDL

movie_url = input("コメントを取得したいアーカイブの URL を貼り付ける：")

ydl_video_opts = {
    'outtmpl' : '%(id)s'+'_.mp4',
    'format' : 'best',
    'writesubtitles' : True,
    'skip_download' : True
}

with YoutubeDL(ydl_video_opts) as ydl:
    result = ydl.download([
        f'{movie_url}'
    ])
