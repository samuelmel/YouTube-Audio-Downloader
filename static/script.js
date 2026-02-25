let pollInterval = null;

async function checkFfmpeg() {
  const res = await fetch('/check');
  const data = await res.json();
  if (!data.ffmpeg) {
    document.getElementById('ffmpeg-warn').style.display = 'block';
  }
}

async function startDownload() {
  const url = document.getElementById('url-input').value.trim();
  if (!url) {
    alert('Paste a YouTube link!');
    return;
  }

  const format = document.getElementById('format-select').value;
  const quality = document.getElementById('quality-select').value;

  // Reset UI
  document.getElementById('download-btn').disabled = true;
  document.getElementById('status-box').style.display = 'flex';
  document.getElementById('save-btn').style.display = 'none';
  document.getElementById('progress-fill').style.width = '0%';
  document.getElementById('status-msg').className = 'status-msg';
  document.getElementById('status-msg').textContent = 'Starting...';

  const res = await fetch('/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, format, quality })
  });

  const data = await res.json();
  if (!data.job_id) {
    showError('Error starting download.');
    return;
  }

  pollInterval = setInterval(() => pollStatus(data.job_id), 800);
}

async function pollStatus(jobId) {
  const res = await fetch(`/status/${jobId}`);
  const data = await res.json();

  document.getElementById('progress-fill').style.width = data.progress + '%';
  document.getElementById('status-msg').textContent = data.message || '...';

  if (data.status === 'done') {
    clearInterval(pollInterval);
    document.getElementById('download-btn').disabled = false;
    const saveBtn = document.getElementById('save-btn');
    saveBtn.href = `/file/${jobId}`;
    saveBtn.style.display = 'block';
    document.getElementById('status-msg').textContent = '✅ ' + (data.title || 'Done!');
  } else if (data.status === 'error') {
    clearInterval(pollInterval);
    showError(data.message);
    document.getElementById('download-btn').disabled = false;
  }
}

function showError(msg) {
  const el = document.getElementById('status-msg');
  el.className = 'status-msg error';
  el.textContent = '❌ ' + msg;
}

checkFfmpeg();