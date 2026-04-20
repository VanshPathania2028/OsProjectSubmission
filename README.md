# File System Recovery & Optimization Tool

A comprehensive tool for simulating file system operations, managing disk space, implementing recovery mechanisms, and optimizing file access performance.

## Features

### 1. **File System Core** (`filesystem_core.py`)
- Inode-based file system architecture
- Block-based storage management
- File and directory metadata tracking
- Checksum-based data integrity verification

### 2. **Free Space Management** (`free_space_manager.py`)
- Bitmap-based free space allocation
- Three allocation strategies:
  - **First Fit**: Allocates first available space
  - **Best Fit**: Allocates smallest sufficient space
  - **Worst Fit**: Allocates largest available space
- Fragmentation tracking and analysis
- Defragmentation engine

### 3. **Directory Management** (`directory_manager.py`)
- Hierarchical directory structure
- Directory creation and deletion
- File creation and deletion
- Directory traversal and path resolution
- Directory statistics and analysis

### 4. **File Access Optimization** (`file_access_optimizer.py`)
- LRU (Least Recently Used) caching
- Predictive read-ahead for sequential access patterns
- Cache hit/miss statistics
- Access pattern analysis
- Performance metrics

### 5. **Recovery Management** (`recovery_manager.py`)
- Checkpoint-based recovery system
- Corruption detection:
  - Orphaned inode detection
  - Circular reference detection
  - Block checksum verification
- Deleted file recovery registry
- Disk crash simulation
- File system repair capabilities

### 6. **Disk Simulator** (`disk_simulator.py`)
- Integrated simulator combining all components
- File operations (create, read, write, delete)
- Directory operations
- Recovery and repair operations
- State export/import (JSON)
- Comprehensive statistics and reporting

### 7. **Interactive CLI** (`main.py`)
- User-friendly command-line interface
- Multiple operation menus
- Demo scenarios
- Step-by-step guidance

## Installation

### Requirements
- Python 3.7+
- No external dependencies are required for the CLI or test modules
- Flask is required only for the web frontend

### Setup

```bash
cd c:\Users\fst\Desktop\osproject2
python main.py
```

## Usage

### Interactive Mode

Run the interactive tool:
```bash
python main.py
```

### Automated Tests

Run the automated unit tests:
```bash
python -m unittest discover -s tests -v
```

The legacy compatibility runner still works:
```bash
python test_suite.py
```

### React Frontend

The project also includes a Node + React frontend in `frontend/`.

Run it in one terminal:
```bash
python web_app.py
```

Then in a second terminal:
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` for the React UI.

### Programmatic Usage

```python
from disk_simulator import DiskSimulator

# Initialize simulator
sim = DiskSimulator(total_blocks=1024, block_size=4096)

# Create file system structure
docs_dir = sim.create_directory("documents")
file_id = sim.create_file("readme.txt", 2048, docs_dir)

# Write data
sim.write_file(file_id, b"File content here")

# Create checkpoint
checkpoint = sim.checkpoint("Before changes")

# Perform operations
sim.read_file(file_id)

# Check statistics
stats = sim.get_statistics()
print(stats)

# Optimize
optimization = sim.optimize()
print(optimization)
```

## Key Concepts

### Inodes
- Represent file and directory metadata
- Contain file size, timestamps, permissions, block pointers
- Each inode has unique ID
- Root directory has inode ID 0

### Blocks
- Fixed-size units of disk storage (default 4096 bytes)
- Allocated based on file size requirements
- Tracked in bitmap for allocation status
- Include checksums for integrity

### Free Space Management Strategies

#### First Fit
- Allocates first available space
- Fast but can cause fragmentation
- Good for quick allocations

#### Best Fit
- Allocates smallest sufficient space
- Minimizes fragmentation
- Reduces unused space within blocks

#### Worst Fit
- Allocates largest available space
- Tries to keep large gaps available
- Good for maintaining flexibility

### Recovery Checkpoints
- Snapshots of entire file system state
- Can restore to any previous checkpoint
- Includes inode and block state
- Timestamped for tracking

### Crash Simulation
- **Light**: Damages 5-10% of blocks
- **Moderate**: Damages 20-40% of blocks
- **Severe**: Damages 50%+ of blocks

## Demo Scenarios

### Scenario 1: Normal Operations
```python
sim = DiskSimulator(512, 4096)
docs = sim.create_directory("documents")
file = sim.create_file("readme.txt", 2048, docs)
sim.write_file(file, b"Important content")
data = sim.read_file(file)
```

### Scenario 2: Crash & Recovery
```python
sim = DiskSimulator(256, 4096)
file = sim.create_file("data.txt", 1024)
sim.write_file(file, b"Critical data")

checkpoint = sim.checkpoint("Safe state")
damage = sim.simulate_crash('moderate')

# Check corruption
issues = sim.check_integrity()

# Recover
sim.recover_from_crash(checkpoint)
```

### Scenario 3: Optimization
```python
sim = DiskSimulator(512, 4096)

# Create files with access pattern
for i in range(10):
    f = sim.create_file(f"file_{i}.dat", 2048)
    sim.read_file(f)

# Optimize
result = sim.optimize()
print(f"Cache hit rate: {result['cache_statistics']['hit_rate']*100}%")
print(f"Fragmentation reduced by: {result['defragmentation']['gaps_consolidated']} gaps")
```

## File Structure

```
osproject2/
├── filesystem_core.py          # Core file system structures
├── free_space_manager.py       # Space allocation strategies
├── directory_manager.py        # Directory operations
├── file_access_optimizer.py    # Caching and optimization
├── recovery_manager.py         # Recovery mechanisms
├── disk_simulator.py           # Main simulator
├── main.py                     # Interactive CLI
├── test_suite.py              # Comprehensive tests
└── README.md                   # Documentation
```

## API Reference

### DiskSimulator Class

#### File Operations
```python
create_file(filename: str, file_size: int, parent_dir_id: int = 0) -> Optional[int]
delete_file(inode_id: int) -> bool
write_file(inode_id: int, data: bytes) -> bool
read_file(inode_id: int) -> Optional[bytes]
```

#### Directory Operations
```python
create_directory(dirname: str, parent_dir_id: int = 0) -> Optional[int]
list_directory(dir_id: int = 0) -> List[dict]
```

#### Recovery Operations
```python
checkpoint(description: str = "") -> Optional[int]
simulate_crash(severity: str = 'moderate') -> dict
recover_from_crash(checkpoint_id: int = None) -> bool
check_integrity() -> dict
repair() -> dict
```

#### Optimization
```python
optimize() -> dict
get_statistics() -> dict
export_state(filename: str = "filesystem_state.json") -> bool
import_state(filename: str = "filesystem_state.json") -> bool
```

## Performance Characteristics

### Time Complexity
- File creation: O(1)
- File deletion: O(1) average
- Directory listing: O(n) where n = number of files
- Crash recovery: O(total_blocks + total_inodes)
- Defragmentation: O(total_blocks)

### Space Complexity
- Bitmap allocation: O(total_blocks)
- Cache: O(cache_size)
- Inode table: O(num_inodes)

## Examples

### Running Test Suite
```bash
python test_suite.py
```

Tests include:
- File system operations
- Allocation strategies comparison
- Access optimization
- Crash recovery
- Fragmentation/defragmentation
- File recovery
- Checkpoint system
- Performance metrics

### Real-World Scenarios

1. **Database Backup**: Regular checkpoints before critical operations
2. **Log File Management**: Monitor fragmentation and optimize placement
3. **Media Storage**: Track file access patterns for optimization
4. **System Recovery**: Test recovery procedures before production deployment

## Advanced Features

### Defragmentation Analysis
```python
fsm = sim.free_space_manager
before = fsm.get_free_space_info()
result = fsm.defragment()
after = result['after']

print(f"Gaps before: {before['num_gaps']}")
print(f"Gaps after: {after['num_gaps']}")
```

### Cache Performance Monitoring
```python
opt = sim.file_access_optimizer
stats = opt.get_cache_stats()
patterns = opt.analyze_access_patterns()

print(f"Hit rate: {stats['hit_rate']*100}%")
print(f"Sequentiality: {patterns['sequentiality_ratio']*100}%")
```

### Corruption Detection
```python
issues = sim.check_integrity()
if not issues['filesystem_healthy']:
    for issue in issues['issues']:
        print(f"Issue: {issue['type']} - Severity: {issue['severity']}")
```

## Configuration

### File System Parameters
```python
sim = DiskSimulator(
    total_blocks=1024,      # Number of disk blocks
    block_size=4096         # Bytes per block
)
```

### Cache Configuration
```python
sim.file_access_optimizer = FileAccessOptimizer(
    cache_size=128,         # Number of blocks to cache
    block_size=4096         # Block size
)
```

### Allocation Strategy
```python
# Available: 'first_fit', 'best_fit', 'worst_fit'
sim.free_space_manager.set_allocation_strategy('best_fit')
```

## Troubleshooting

### File Creation Fails
- Check available free space: `sim.get_statistics()`
- Verify parent directory exists: `sim.check_integrity()`

### Recovery Fails
- Check available checkpoints: `recovery_manager.recovery_points`
- Verify checkpoint ID
- Check file system corruption first

### Performance Issues
- Analyze cache hit rate: `file_access_optimizer.get_cache_stats()`
- Check fragmentation: `free_space_manager.get_free_space_info()`
- Run defragmentation: `sim.optimize()`

## Contributing

To extend this tool:

1. Add new allocation strategies in `free_space_manager.py`
2. Implement additional recovery techniques in `recovery_manager.py`
3. Add optimization algorithms to `file_access_optimizer.py`
4. Create new demo scenarios in `test_suite.py`

## License

This is an educational tool for operating systems learning.

## References

- Unix File System Architecture
- Ext4 Filesystem Implementation
- Recovery and Backup Strategies
- Cache Replacement Policies (LRU)
- Fragmentation Management Techniques

## Author

File System Recovery & Optimization Tool
Created as a comprehensive OS project for file system management education.
