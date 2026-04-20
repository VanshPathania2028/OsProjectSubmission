"""
Web-based Frontend for File System Recovery & Optimization Tool
Flask application with REST API for the disk simulator
"""


from flask import Flask, render_template, request, jsonify, session, send_from_directory
from disk_simulator import DiskSimulator
import json
import uuid

app = Flask(__name__)
app.secret_key = 'filesystem_recovery_tool_secret'

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Store simulator instances per session
simulators = {}

def get_simulator():
    """Get or create simulator for current session."""
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
    
    if session_id not in simulators:
        simulators[session_id] = DiskSimulator(512, 4096)
    
    return simulators[session_id]

@app.route('/')
def index():
    """Main dashboard - React app."""
    return send_from_directory('static', 'index.html')

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Initialize file system."""
    data = request.json
    total_blocks = data.get('total_blocks', 512)
    block_size = data.get('block_size', 4096)
    
    sim = DiskSimulator(total_blocks, block_size)
    session_id = session.get('session_id', str(uuid.uuid4()))
    session['session_id'] = session_id
    simulators[session_id] = sim
    
    stats = sim.get_statistics()
    return jsonify({
        'success': True,
        'message': f'File system initialized with {total_blocks} blocks',
        'statistics': stats
    })

@app.route('/api/statistics', methods=['GET'])
def api_statistics():
    """Get file system statistics."""
    sim = get_simulator()
    stats = sim.get_statistics()
    return jsonify({
        'success': True,
        'statistics': stats
    })

@app.route('/api/file/create', methods=['POST'])
def api_create_file():
    """Create a file."""
    sim = get_simulator()
    data = request.json
    
    filename = data.get('filename', 'untitled.txt')
    file_size = data.get('file_size', 1024)
    parent_dir_id = data.get('parent_dir_id', 0)
    
    try:
        file_id = sim.create_file(filename, file_size, parent_dir_id)
        if file_id:
            return jsonify({
                'success': True,
                'message': f'File "{filename}" created',
                'file_id': file_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create file'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/file/delete/<int:file_id>', methods=['DELETE'])
def api_delete_file(file_id):
    """Delete a file."""
    sim = get_simulator()
    
    try:
        success = sim.delete_file(file_id)
        if success:
            return jsonify({
                'success': True,
                'message': f'File {file_id} deleted'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete file'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/file/write/<int:file_id>', methods=['POST'])
def api_write_file(file_id):
    """Write data to file."""
    sim = get_simulator()
    data = request.json
    file_data = data.get('data', '').encode()
    
    try:
        success = sim.write_file(file_id, file_data)
        if success:
            return jsonify({
                'success': True,
                'message': f'Data written to file {file_id}',
                'bytes_written': len(file_data)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to write file'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/file/read/<int:file_id>', methods=['GET'])
def api_read_file(file_id):
    """Read data from file."""
    sim = get_simulator()
    
    try:
        data = sim.read_file(file_id)
        if data:
            return jsonify({
                'success': True,
                'data': data.decode(errors='ignore'),
                'bytes_read': len(data)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to read file'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/directory/create', methods=['POST'])
def api_create_directory():
    """Create a directory."""
    sim = get_simulator()
    data = request.json
    
    dirname = data.get('dirname', 'untitled')
    parent_dir_id = data.get('parent_dir_id', 0)
    
    try:
        dir_id = sim.create_directory(dirname, parent_dir_id)
        if dir_id:
            return jsonify({
                'success': True,
                'message': f'Directory "{dirname}" created',
                'dir_id': dir_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create directory'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/directory/list/<int:dir_id>', methods=['GET'])
def api_list_directory(dir_id):
    """List directory contents."""
    sim = get_simulator()
    
    try:
        contents = sim.list_directory(dir_id)
        return jsonify({
            'success': True,
            'contents': contents,
            'count': len(contents)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/checkpoint/create', methods=['POST'])
def api_create_checkpoint():
    """Create recovery checkpoint."""
    sim = get_simulator()
    data = request.json
    description = data.get('description', 'Checkpoint')
    
    try:
        checkpoint_id = sim.checkpoint(description)
        if checkpoint_id is not None:
            return jsonify({
                'success': True,
                'message': f'Checkpoint {checkpoint_id} created',
                'checkpoint_id': checkpoint_id
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create checkpoint'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/crash/simulate', methods=['POST'])
def api_simulate_crash():
    """Simulate disk crash."""
    sim = get_simulator()
    data = request.json
    severity = data.get('severity', 'moderate')
    
    try:
        damage = sim.simulate_crash(severity)
        return jsonify({
            'success': True,
            'severity': damage['severity'],
            'damaged_blocks': len(damage['damaged_blocks']),
            'recommendation': damage['recovery_recommendation']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/recovery/recover/<int:checkpoint_id>', methods=['POST'])
def api_recover(checkpoint_id):
    """Recover from checkpoint."""
    sim = get_simulator()
    
    try:
        success = sim.recover_from_crash(checkpoint_id)
        if success:
            return jsonify({
                'success': True,
                'message': f'Recovered from checkpoint {checkpoint_id}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Recovery failed'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/integrity/check', methods=['GET'])
def api_check_integrity():
    """Check file system integrity."""
    sim = get_simulator()
    
    try:
        integrity = sim.check_integrity()
        return jsonify({
            'success': True,
            'healthy': integrity['filesystem_healthy'],
            'total_issues': integrity['total_issues'],
            'issues': integrity['issues']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/repair', methods=['POST'])
def api_repair():
    """Repair file system."""
    sim = get_simulator()
    
    try:
        result = sim.repair()
        return jsonify({
            'success': True,
            'issues_detected': result['issues_detected'],
            'issues_repaired': result['issues_repaired'],
            'actions': result['actions_taken']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    """Optimize file system."""
    sim = get_simulator()
    
    try:
        result = sim.optimize()
        return jsonify({
            'success': True,
            'cache_hit_rate': f"{result['cache_statistics']['hit_rate']*100:.1f}%",
            'gaps_consolidated': result['defragmentation']['gaps_consolidated'],
            'fragmentation_before': f"{result['defragmentation']['before']['fragmentation_ratio']:.2f}",
            'fragmentation_after': f"{result['defragmentation']['after']['fragmentation_ratio']:.2f}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/export', methods=['GET'])
def api_export():
    """Export file system state."""
    sim = get_simulator()
    
    try:
        filename = 'filesystem_export.json'
        success = sim.export_state(filename)
        if success:
            return jsonify({
                'success': True,
                'message': f'Exported to {filename}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Export failed'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

