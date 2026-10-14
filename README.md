# Alzheimer's MRI Detection - Front-End Prototype

Includes: Home, Upload (drag & drop, live preview, validation), Upload-success, About, Contact, and 404/500 pages.

Not included yet: preprocessing, CNN model, prediction, Grad-CAM, PDF report.

## Requirements
- Python 3.9 or newer

## Run

Open a terminal in the project folder (the folder containing `app.py`), then:

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser. Stop the server with `Ctrl+C`.

If PowerShell blocks activation, run this once and retry:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

To use a different port: set the `PORT` environment variable (e.g. `$env:PORT=5001` in PowerShell).
