from flask import Flask, request, render_template, send_file
from yt_dlp import YoutubeDL
import os
import shutil

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", message="Введите URL!")

        try:
            # Настройки для yt-dlp
            output_path = "downloads"
            ydl_opts = {
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            
            # Отправляем файл пользователю
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            return render_template("index.html", message=f"Ошибка: {str(e)}")
    
    return render_template("index.html", message="")

# Очистка папки downloads перед выходом (опционально)
@app.route("/shutdown", methods=["POST"])
def shutdown():
    shutil.rmtree("downloads", ignore_errors=True)
    return "Сервер остановлен"

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    app.run(debug=True)