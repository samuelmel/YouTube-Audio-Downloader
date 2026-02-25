#!/usr/bin/env python3
"""
YouTube Audio Downloader - Web Interface
"""

import os
import sys
import shutil
import threading
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template

try:
    import yt_dlp
except ImportError:
    os.system(f"{sys.executable} -m pip install yt-dlp --break-system-packages")
    import yt_dlp

app = Flask(__name__)

# Downloads directory (in the same folder as the script)
DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Dictionary to track progress of each job
jobs = {}


def check_ffmpeg():
    return shutil.which('ffmpeg') is not None


def download_worker(job_id, url, format_type, quality):
    """Executes the download in a separate thread"""
    jobs[job_id]['status'] = 'downloading'
    jobs[job_id]['progress'] = 0

    def progress_hook(d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                pct = d['downloaded_bytes'] / d['total_bytes'] * 100
                jobs[job_id]['progress'] = round(pct, 1)
                jobs[job_id]['message'] = f"Downloading... {pct:.1f}%"
            elif 'downloaded_bytes' in d:
                mb = d['downloaded_bytes'] / (1024 * 1024)
                jobs[job_id]['message'] = f"Downloading... {mb:.1f} MB"
        elif d['status'] == 'finished':
            jobs[job_id]['progress'] = 95
            jobs[job_id]['message'] = "Converting audio..."

    output_template = str(DOWNLOAD_DIR / f"{job_id}_%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }

    if format_type in ['mp3', 'wav', 'opus', 'm4a']:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_type,
            'preferredquality': quality,
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            filename_base = ydl.prepare_filename(info)
            base = os.path.splitext(filename_base)[0]
            final_file = f"{base}.{format_type}"

            if not os.path.exists(final_file):
                # Try to find the generated file
                for f in DOWNLOAD_DIR.glob(f"{job_id}_*"):
                    final_file = str(f)
                    break

            jobs[job_id]['status'] = 'done'
            jobs[job_id]['progress'] = 100
            jobs[job_id]['message'] = 'Done!'
            jobs[job_id]['file'] = final_file
            jobs[job_id]['title'] = title

    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['message'] = str(e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check')
def check():
    return jsonify({'ffmpeg': check_ffmpeg()})


@app.route('/download', methods=['POST'])
def start_download():
    data = request.json
    url = data.get('url', '').strip()
    format_type = data.get('format', 'mp3')
    quality = data.get('quality', '320')

    if not url:
        return jsonify({'error': 'Invalid URL'}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {'status': 'queued', 'progress': 0, 'message': 'In queue...'}

    t = threading.Thread(target=download_worker, args=(job_id, url, format_type, quality), daemon=True)
    t.start()

    return jsonify({'job_id': job_id})


@app.route('/status/<job_id>')
def get_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)


@app.route('/file/<job_id>')
def get_file(job_id):
    job = jobs.get(job_id)
    if not job or job.get('status') != 'done':
        return jsonify({'error': 'File not available'}), 404

    filepath = job.get('file')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    print("=" * 50)
    print("🎵 YouTube Audio Downloader - Web")
    print("=" * 50)
    if not check_ffmpeg():
        print("⚠️  FFmpeg not found! Conversion may fail.")
    print(f"📁 Downloads saved in: {DOWNLOAD_DIR}")
    print(f"\n🌐 Open in browser: http://localhost:5000\n")
    app.run(debug=False, host='0.0.0.0', port=5000)