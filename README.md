# 🎵 YouTube Audio Downloader - Web

🚀 **Live Demo:** (https://youtube-audio-downloader-4cee.onrender.com)

A simple and intuitive web application that allows users to download audio from YouTube videos directly from the browser.

Paste the video link, choose the format, and download the audio in seconds.

---

## ✨ Features

- Download audio from YouTube videos
- Automatic audio conversion using FFmpeg
- Clean and simple interface
- Server-side processing
- Production deployment on Railway

---

## 🛠 Tech Stack

- Python
- Flask
- yt-dlp
- FFmpeg
- Railway (Cloud Hosting)

---

## ☁️ Deployment

This application is deployed using Railway as a cloud web service.

The production environment includes:
- Python runtime
- yt-dlp for media extraction
- FFmpeg for audio conversion

The app runs as a public web service accessible via the live demo URL.
---

## ▶ Run Locally

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

Create and activate a virtual environment:

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install FFmpeg (required for audio conversion):

**Windows**
```bash
winget install ffmpeg
```
Or download manually at: https://www.gyan.dev/ffmpeg/builds/

**macOS**
```bash
brew install ffmpeg
```

**Ubuntu/Debian**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Fedora**
```bash
sudo dnf install ffmpeg
```

**Arch Linux**
```bash
sudo pacman -S ffmpeg
```

Run the application:

```bash
python app.py
```

Open your browser at:

```
http://localhost:5000
```

---
## ⚠️ Disclaimer

This project is intended for educational purposes only.
Users are responsible for complying with YouTube's Terms of Service and applicable copyright laws.
---

## 👨‍💻 Author

**Samuel Mendes** — Computer Science Student | Backend & Automation Developer

GitHub: https://github.com/samuelmel
