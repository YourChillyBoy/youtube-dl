from yt_dlp import YoutubeDL

def download_video(url, output_path="downloads"):
    try:
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Шаблон имени файла
            'format': 'bestvideo+bestaudio/best',  # Выбираем лучшее качество
            'merge_output_format': 'mp4',  # Объединяем в mp4
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path, f"Видео '{info['title']}' успешно скачано!"
    except Exception as e:
        return None, f"Ошибка: {str(e)}"