# 🎵 YouTube Audio Downloader - Web

A simple web interface to download audio from YouTube.
Paste the link, choose the format, and click download.

---

## ▶ How to Run

### Windows

1. Install Python: https://www.python.org/downloads/
2. Open **Command Prompt** in the project folder
3. Run:

```
pip install flask yt-dlp
python app.py
```

4. Open your browser at: **http://localhost:5000**

---

### macOS

1. Open **Terminal** in the project folder
2. Run:

```bash
pip3 install flask yt-dlp
python3 app.py
```

3. Open your browser at: **http://localhost:5000**

---

### Linux

1. Open **Terminal** in the project folder
2. Run:

```bash
pip install flask yt-dlp --break-system-packages
python3 app.py
```

3. Open your browser at: **http://localhost:5000**

---

## ⚠️ FFmpeg (required for audio conversion)

### Windows
```
winget install ffmpeg
```
Or download from: https://www.gyan.dev/ffmpeg/builds/

### macOS
```
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```
sudo apt install ffmpeg
```

---

