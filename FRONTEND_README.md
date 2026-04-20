# Web Frontend for File System Recovery Tool

Modern frontend options for the File System Recovery & Optimization Tool.

The project now includes:
- A legacy Flask-rendered dashboard in `templates/` and `static/`
- A new Node + React frontend in `frontend/` powered by Vite

## Setup

### Prerequisites
- Python 3.7+
- Node.js 18+ for the React frontend
- Flask library

### Installation

1. **Install Flask**
```bash
pip install flask
```

2. **Navigate to project directory**
```bash
cd c:\Users\fst\Desktop\osproject2
```

3. **Run the Flask API**
```bash
python web_app.py
```

4. **Run the React frontend**
```bash
cd frontend
npm install
npm run dev
```

5. **Open in browser**
- React frontend: `http://localhost:5173`
- Flask backend: `http://localhost:5000`

## Features

### React Control Room
- Built with React and Vite
- Talks to Flask through a Vite dev proxy
- Interactive operations feed
- Single-page dashboard workflow

### Legacy Dashboard
- Flask-rendered HTML template
- Kept for fallback/simple usage

### Modern Web Interface
- Clean, intuitive dashboard
- Real-time statistics and updates
- Responsive design (works on mobile, tablet, desktop)
- Professional styling with gradients and animations

### File System Operations
- Create/delete files
- Write/read file data
- Create/navigate directories
- List directory contents

### Recovery & Backup
- Create recovery checkpoints
- Simulate disk crashes (light/moderate/severe)
- Check file system integrity
- Automatic repair functionality
- Restore from checkpoints

### Optimization
- One-click optimization
- Cache performance metrics
- Fragmentation analysis
- Defragmentation
- Performance tuning

### Real-time Statistics
- Total blocks and capacity
- Allocation information
- Fragmentation analysis
- Cache hit rates
- Live updates

## File Structure

```text
osproject2/
|-- frontend/                # React + Vite frontend
|-- web_app.py               # Flask backend
|-- templates/
|   `-- dashboard.html       # Main HTML interface
`-- static/
    |-- style.css            # Styling
    `-- script.js            # Frontend logic
```

## API Endpoints

### System Operations
- `POST /api/initialize` - Initialize file system
- `GET /api/statistics` - Get system statistics

### File Operations
- `POST /api/file/create` - Create file
- `POST /api/file/write/<id>` - Write to file
- `GET /api/file/read/<id>` - Read file
- `DELETE /api/file/delete/<id>` - Delete file

### Directory Operations
- `POST /api/directory/create` - Create directory
- `GET /api/directory/list/<id>` - List contents

### Recovery Operations
- `POST /api/checkpoint/create` - Create checkpoint
- `POST /api/recovery/recover/<id>` - Recover from checkpoint

### Crash Simulation
- `POST /api/crash/simulate` - Simulate crash
- `GET /api/integrity/check` - Check integrity
- `POST /api/repair` - Repair filesystem

### Optimization
- `POST /api/optimize` - Optimize filesystem
- `GET /api/export` - Export state

## Usage Guide

### 1. Initialize File System
- Go to "Initialize" section
- Set total blocks and block size
- Click "Initialize"

### 2. Create Files and Directories
- Create directories in "Directories" section
- Create files in "Files" section
- Write/read data using file operations

### 3. Create Checkpoints
- Before critical operations
- Give descriptive names
- Use for recovery if needed

### 4. Simulate Crashes
- Choose severity level (light/moderate/severe)
- Check integrity after crash
- Repair if needed
- Recover from checkpoint

### 5. Optimize System
- Monitor fragmentation
- Run optimization
- Check improved cache hit rate

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Keyboard Shortcuts

- `Alt + I` - Initialize section
- `Alt + F` - Files section
- `Alt + D` - Directories section
- `Alt + R` - Recovery section

(Shortcuts can be added via HTML)

## Performance

- Fast response times (<100ms for most operations)
- Smooth animations and transitions
- Efficient AJAX calls
- Real-time status updates

## Configuration

Edit `web_app.py` to change:

```python
# Port
app.run(debug=True, port=5000)  # Change port number

# Debug mode (set to False in production)
app.run(debug=True)  # Change to False

# Session timeout
app.permanent_session_lifetime = timedelta(days=1)
```

## Troubleshooting

### Port Already in Use
```bash
python web_app.py
# If port 5000 is busy, change it in web_app.py
```

### Flask Not Found
```bash
pip install flask --upgrade
```

### Session Issues
- Clear browser cookies
- Use private/incognito window
- Restart Flask app

### File Not Working
- Check file ID is correct
- Ensure file system initialized
- Check file size is reasonable

## Development

### Adding New Features

1. **Add API endpoint in `web_app.py`**
```python
@app.route("/api/newfeature", methods=["POST"])
def api_new_feature():
    # Implementation
    return jsonify({"success": True})
```

2. **Add button in `templates/dashboard.html`**
```html
<button onclick="newFeature()" class="btn btn-primary">Feature</button>
```

3. **Add JavaScript function in `static/script.js`**
```javascript
async function newFeature() {
    // Call API and handle response
}
```
