# Quickstart: OS File System Simulator (Merged Frontend/Backend)

## Prerequisites
- Python 3.8+
- Node.js 18+

## 1. Install Backend Deps
```
pip install -r requirements.txt
```

## 2. Dev Mode (Hot Reload UI)
Terminal 1 (Backend/API):
```
python web_app.py
```
Backend: http://localhost:5000/api (Flask)

Terminal 2 (Frontend):
```
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173 (React + API proxy)

## 3. Prod Mode (Single Server)
```
cd frontend
npm install
npm run build:merge
python web_app.py
```
Full app: http://localhost:5000 (React UI + API)

## 4. CLI Mode (No UI)
```
python main.py
```

## Verify
- Open browser to UI URL
- Initialize FS, create files, simulate crash, recover
- Check Network tab for /api calls

**Demo**: Use presentation_materials/quick_demo_commands.bat
