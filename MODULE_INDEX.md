# File System Recovery & Optimization Tool - Module Index

## Project Files

### Core Modules (Foundation)

#### 1. **filesystem_core.py** - Core File System Architecture
- **INode Class**: Represents file/directory metadata
- **Block Class**: Represents disk blocks with data and checksums
- **FileSystemCore Class**: Main file system engine
- **Key Functions**:
  - `allocate_inode()` - Create new file/directory inode
  - `deallocate_inode()` - Mark inode as deleted
  - `write_block()` - Write data to disk block
  - `read_block()` - Read data from disk block
  - `get_system_info()` - Get file system statistics

#### 2. **free_space_manager.py** - Space Allocation Management
- **FreeSpaceManager Class**: Manages disk space allocation
- **Three Allocation Strategies**:
  - First Fit - Fastest allocation
  - Best Fit - Minimizes fragmentation
  - Worst Fit - Maximizes flexibility
- **Key Functions**:
  - `allocate_blocks()` - Allocate disk blocks
  - `deallocate_blocks()` - Free disk blocks
  - `defragment()` - Consolidate free space
  - `get_free_space_info()` - Fragmentation analysis
  - `set_allocation_strategy()` - Switch strategies

#### 3. **directory_manager.py** - Hierarchical Organization
- **DirectoryManager Class**: Manages directory structure
- **Key Functions**:
  - `create_directory()` - Create new directory
  - `delete_directory()` - Remove empty directory
  - `create_file()` - Create new file
  - `delete_file()` - Remove file
  - `list_directory()` - Show directory contents
  - `find_file()` - Search for file recursively
  - `get_path()` - Get full file path
  - `get_directory_stats()` - Directory statistics

#### 4. **file_access_optimizer.py** - Performance Optimization
- **CacheEntry Class**: Represents cached block data
- **FileAccessOptimizer Class**: Implements caching and optimization
- **Key Functions**:
  - `read_block()` - Read with caching
  - `write_block()` - Write with caching
  - `analyze_access_patterns()` - Pattern analysis
  - `get_cache_stats()` - Cache performance metrics
  - `_read_ahead()` - Predictive caching
  - `optimize_block_placement()` - Hot/cold block analysis

#### 5. **recovery_manager.py** - Disaster Recovery
- **RecoveryPoint Class**: Checkpoint snapshot
- **RecoveryManager Class**: Handles recovery operations
- **Key Functions**:
  - `create_checkpoint()` - Create recovery point
  - `detect_corruption()` - Find file system issues
  - `recover_from_checkpoint()` - Restore state
  - `register_deleted_file()` - Track deleted files
  - `recover_deleted_file()` - Restore deleted files
  - `simulate_disk_crash()` - Simulate various crash scenarios
  - `repair_filesystem()` - Fix corruption

### Integration & Application

#### 6. **disk_simulator.py** - Main Simulator Engine
- **DiskSimulator Class**: Combines all components
- **Key Functions**:
  - `create_file()` - Create and allocate file
  - `delete_file()` - Delete and free file
  - `write_file()` - Write file data
  - `read_file()` - Read file data
  - `create_directory()` - Create directory
  - `list_directory()` - List contents
  - `checkpoint()` - Create recovery point
  - `simulate_crash()` - Simulate crash
  - `recover_from_crash()` - Recover from crash
  - `check_integrity()` - Find problems
  - `repair()` - Fix problems
  - `optimize()` - Optimize system
  - `get_statistics()` - System metrics
  - `export_state()` - Save to JSON
  - `import_state()` - Load from JSON

#### 7. **main.py** - Interactive Command-Line Interface
- **FileSystemTool Class**: Interactive menu system
- **Menus**:
  - File Operations (create/delete/read/write)
  - Directory Operations (create/list/navigate)
  - Recovery Operations (checkpoint/crash/repair)
  - Optimization Operations (optimize/tune)
  - Statistics Display
  - Demo Scenarios
- **Features**:
  - Step-by-step guidance
  - Real-time results
  - Error handling
  - Multiple demo scenarios

### Testing & Examples

#### 8. **test_suite.py** - Comprehensive Testing
- **8 Test Categories**:
  1. File system operations
  2. Free space management
  3. File access optimization
  4. Crash recovery
  5. Fragmentation/defragmentation
  6. File recovery
  7. Checkpoint system
  8. Performance metrics

#### 9. **usecases.py** - Real-World Examples
- **6 Practical Use Cases**:
  1. Database backup system
  2. Log file optimization
  3. Media storage management
  4. System file migration
  5. Severe fragmentation recovery
  6. Performance tuning & comparison

### Documentation

#### **README.md** - Comprehensive Documentation
- Project overview
- Feature descriptions
- Installation instructions
- API reference
- Configuration options
- Performance characteristics
- Troubleshooting guide
- Real-world scenarios

#### **QUICKSTART.md** - Quick Start Guide
- Installation steps
- Module overview
- Common tasks with examples
- Menu navigation
- Key concepts
- Performance tips
- Troubleshooting
- Hardware requirements

#### **requirements.txt** - Dependencies & Setup
- Python version requirement
- No external dependencies
- Installation methods
- Virtual environment setup
- Optional development tools
- Hardware requirements

#### **PROJECT_SUMMARY.txt** - Complete Project Summary
- Project overview
- Components description
- Feature list
- Statistics
- Usage modes
- Quick start
- Architecture design
- Testing results
- Completion checklist

#### **This File** - Module Index
- File descriptions
- Function references
- Quick navigation

---

## Quick Navigation Guide

### By Task

**I want to test the system:**
→ `python test_suite.py`

**I want to explore use cases:**
→ `python usecases.py`

**I want interactive menu:**
→ `python main.py`

**I want to use it in my code:**
```python
from disk_simulator import DiskSimulator
sim = DiskSimulator()
```

### By Module

**Understanding file systems:**
→ `filesystem_core.py`

**Learning about allocation:**
→ `free_space_manager.py`

**Directory management:**
→ `directory_manager.py`

**Performance optimization:**
→ `file_access_optimizer.py`

**Recovery mechanisms:**
→ `recovery_manager.py`

**Integration:**
→ `disk_simulator.py`

### By Documentation

**Get started quickly:**
→ `QUICKSTART.md`

**Full documentation:**
→ `README.md`

**Project overview:**
→ `PROJECT_SUMMARY.txt`

**Dependencies:**
→ `requirements.txt`

---

## Key Classes Summary

### FileSystemCore
- Creates and manages inodes
- Manages disk blocks
- Tracks allocations

### FreeSpaceManager
- Bitmap-based allocation
- Multiple strategies
- Defragmentation

### DirectoryManager
- Hierarchical file structure
- File/directory operations
- Navigation

### FileAccessOptimizer
- Block caching (LRU)
- Read-ahead prediction
- Performance analysis

### RecoveryManager
- Checkpoint creation
- Corruption detection
- System repair
- File recovery

### DiskSimulator
- Coordinates all components
- Provides unified interface
- Statistics and reporting

### FileSystemTool
- Interactive menu interface
- User guidance
- Demo scenarios

---

## Data Structures

### INode
```
- inode_id: Unique identifier
- filename: File/directory name
- file_size: Size in bytes
- created_time: Creation timestamp
- modified_time: Last modification
- accessed_time: Last access
- permissions: Unix-style permissions
- owner: File owner
- block_pointers: List of block IDs
- is_directory: Type flag
- parent_inode: Parent directory ID
- directory_entries: Child files/dirs (if directory)
- is_allocated: Allocation status
```

### Block
```
- block_id: Unique identifier
- data: Block content (bytearray)
- is_allocated: Allocation status
- checksum: Data integrity check
```

### CacheEntry
```
- block_id: Cached block ID
- data: Block data (bytes)
- timestamp: Cache time
- access_count: Total accesses
- last_accessed: Recent access time
```

### RecoveryPoint
```
- checkpoint_id: Unique identifier
- timestamp: Creation time
- description: Checkpoint note
- filesystem_state: Full state snapshot
- inode_backup: Inode table copy
- block_map_backup: Block allocation copy
```

---

## API Quick Reference

### Create File System
```python
from disk_simulator import DiskSimulator
sim = DiskSimulator(total_blocks=1024, block_size=4096)
```

### File Operations
```python
file_id = sim.create_file("test.txt", 2048)
sim.write_file(file_id, b"data")
data = sim.read_file(file_id)
sim.delete_file(file_id)
```

### Directory Operations
```python
dir_id = sim.create_directory("documents")
contents = sim.list_directory(dir_id)
```

### Recovery
```python
cp = sim.checkpoint("backup")
sim.recover_from_crash(cp)
issues = sim.check_integrity()
sim.repair()
```

### Optimization
```python
result = sim.optimize()
stats = sim.get_statistics()
```

---

## Version & Status

**Current Version:** 1.0  
**Status:** Complete & Tested  
**Python Required:** 3.7+  
**External Dependencies:** None  
**Lines of Code:** ~3,000  
**Documentation:** ~1,000 lines  
**Test Coverage:** Comprehensive  

---

## Getting Help

1. **Quick Start** → `QUICKSTART.md`
2. **Full Docs** → `README.md`
3. **Examples** → Run `python usecases.py`
4. **Tests** → Run `python test_suite.py`
5. **API** → Check module docstrings and README
6. **Issues** → Check Troubleshooting in README

---

*Last Updated: April 2026*  
*Professional-grade file system simulator for education and testing*
