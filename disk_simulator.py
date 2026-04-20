"""
Disk simulator for testing file system operations and recovery scenarios.
Combines all components to simulate real-world disk operations.
"""

from filesystem_core import FileSystemCore
from free_space_manager import FreeSpaceManager
from directory_manager import DirectoryManager
from file_access_optimizer import FileAccessOptimizer
from recovery_manager import RecoveryManager
from typing import List, Optional, Dict
import json


class DiskSimulator:
    """Comprehensive disk and file system simulator."""
    
    def __init__(self, total_blocks: int = 1024, block_size: int = 4096):
        """Initialize disk simulator with all components."""
        self.total_blocks = total_blocks
        self.block_size = block_size
        
        # Core components
        self.fs_core = FileSystemCore(total_blocks, block_size)
        self.free_space_manager = FreeSpaceManager(total_blocks)
        self.directory_manager = DirectoryManager(self.fs_core)
        self.file_access_optimizer = FileAccessOptimizer(
            cache_size=128,
            block_size=block_size
        )
        self.recovery_manager = RecoveryManager()
        
        self.operation_log: List[dict] = []
    
    def create_file(self, filename: str, file_size: int, 
                   parent_dir_id: int = 0) -> Optional[int]:
        """Create a new file."""
        # Allocate blocks
        num_blocks_needed = (file_size + self.block_size - 1) // self.block_size
        allocated_blocks = self.free_space_manager.allocate_blocks(num_blocks_needed)
        
        if not allocated_blocks:
            return None
        
        # Create file inode
        file_inode = self.directory_manager.create_file(
            filename,
            file_size,
            parent_dir_id
        )
        
        if file_inode:
            file_inode.block_pointers = allocated_blocks
            
            # Mark blocks as allocated in filesystem
            for block_id in allocated_blocks:
                self.fs_core.blocks[block_id].is_allocated = True
            
            self.operation_log.append({
                'operation': 'file_created',
                'filename': filename,
                'file_size': file_size,
                'blocks_allocated': allocated_blocks
            })
            
            return file_inode.inode_id
        
        return None
    
    def delete_file(self, inode_id: int) -> bool:
        """Delete a file and free its blocks."""
        file_inode = self.fs_core.get_inode(inode_id)
        
        if not file_inode or file_inode.is_directory:
            return False
        
        # Register for recovery
        self.recovery_manager.register_deleted_file(
            inode_id,
            file_inode.filename,
            file_inode.file_size,
            file_inode.block_pointers,
            file_inode.parent_inode
        )
        
        # Free blocks
        self.free_space_manager.deallocate_blocks(file_inode.block_pointers)
        for block_id in file_inode.block_pointers:
            self.fs_core.blocks[block_id].is_allocated = False
        
        # Remove from directory
        self.directory_manager.delete_file(inode_id)
        
        self.operation_log.append({
            'operation': 'file_deleted',
            'filename': file_inode.filename,
            'inode_id': inode_id
        })
        
        return True
    
    def write_file(self, inode_id: int, data: bytes) -> bool:
        """Write data to a file."""
        file_inode = self.fs_core.get_inode(inode_id)
        if not file_inode or file_inode.is_directory:
            return False
        
        # Write to blocks using optimizer
        blocks_written = 0
        for i, block_id in enumerate(file_inode.block_pointers):
            block_data = data[i * self.block_size:(i + 1) * self.block_size]
            success = self.file_access_optimizer.write_block(
                block_id,
                block_data,
                self.fs_core.write_block
            )
            if success:
                blocks_written += 1
        
        file_inode.modified_time = __import__('datetime').datetime.now().timestamp()
        
        self.operation_log.append({
            'operation': 'file_written',
            'inode_id': inode_id,
            'blocks_written': blocks_written
        })
        
        return blocks_written == len(file_inode.block_pointers)
    
    def read_file(self, inode_id: int) -> Optional[bytes]:
        """Read data from a file."""
        file_inode = self.fs_core.get_inode(inode_id)
        if not file_inode or file_inode.is_directory:
            return None
        
        data = bytearray()
        for block_id in file_inode.block_pointers:
            block_data = self.file_access_optimizer.read_block(
                block_id,
                self.fs_core.read_block
            )
            if block_data:
                data.extend(block_data)
        
        file_inode.accessed_time = __import__('datetime').datetime.now().timestamp()
        
        self.operation_log.append({
            'operation': 'file_read',
            'inode_id': inode_id,
            'blocks_read': len(file_inode.block_pointers)
        })
        
        return bytes(data[:file_inode.file_size])
    
    def create_directory(self, dirname: str, 
                        parent_dir_id: int = 0) -> Optional[int]:
        """Create a new directory."""
        dir_inode = self.directory_manager.create_directory(dirname, parent_dir_id)
        
        if dir_inode:
            self.operation_log.append({
                'operation': 'directory_created',
                'dirname': dirname,
                'inode_id': dir_inode.inode_id
            })
            return dir_inode.inode_id
        
        return None
    
    def list_directory(self, dir_id: int = 0) -> List[dict]:
        """List directory contents."""
        return self.directory_manager.list_directory(dir_id)
    
    def checkpoint(self, description: str = "") -> Optional[int]:
        """Create a recovery checkpoint."""
        return self.recovery_manager.create_checkpoint(self.fs_core, description)
    
    def simulate_crash(self, severity: str = 'moderate') -> dict:
        """Simulate a disk crash."""
        self.file_access_optimizer.flush_cache()
        return self.recovery_manager.simulate_disk_crash(self.fs_core, severity)
    
    def recover_from_crash(self, checkpoint_id: int = None) -> bool:
        """Recover from crash using a checkpoint."""
        if checkpoint_id is None:
            # Use latest checkpoint
            if self.recovery_manager.recovery_points:
                checkpoint_id = max(self.recovery_manager.recovery_points.keys())
            else:
                return False
        
        success = self.recovery_manager.recover_from_checkpoint(checkpoint_id, self.fs_core)
        
        if success:
            self.file_access_optimizer.flush_cache()
            self.operation_log.append({
                'operation': 'filesystem_recovered',
                'checkpoint_id': checkpoint_id
            })
        
        return success
    
    def check_integrity(self) -> dict:
        """Check file system integrity."""
        corruptions = self.recovery_manager.detect_corruption(self.fs_core)
        
        return {
            'total_issues': len(corruptions),
            'issues': corruptions,
            'filesystem_healthy': len(corruptions) == 0
        }
    
    def repair(self) -> dict:
        """Repair file system."""
        return self.recovery_manager.repair_filesystem(self.fs_core)
    
    def optimize(self) -> dict:
        """Optimize file system."""
        defrag_result = self.free_space_manager.defragment()
        cache_stats = self.file_access_optimizer.get_cache_stats()
        access_patterns = self.file_access_optimizer.analyze_access_patterns()
        
        return {
            'defragmentation': defrag_result,
            'cache_statistics': cache_stats,
            'access_patterns': access_patterns
        }
    
    def get_statistics(self) -> dict:
        """Get comprehensive system statistics."""
        fs_info = self.fs_core.get_system_info()
        space_info = self.free_space_manager.get_free_space_info()
        cache_info = self.file_access_optimizer.get_cache_stats()
        
        return {
            'filesystem': fs_info,
            'free_space': space_info,
            'cache': cache_info,
            'total_operations': len(self.operation_log),
            'recovery_points': len(self.recovery_manager.recovery_points)
        }
    
    def export_state(self, filename: str = "filesystem_state.json") -> bool:
        """Export file system state to JSON."""
        try:
            state = {
                'timestamp': __import__('datetime').datetime.now().isoformat(),
                'filesystem': self.fs_core.get_system_info(),
                'inodes': {
                    str(k): v.to_dict() 
                    for k, v in self.fs_core.inodes.items()
                },
                'free_space': self.free_space_manager.get_free_space_info(),
                'statistics': self.get_statistics(),
                'operation_log': self.operation_log
            }
            
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error exporting state: {e}")
            return False
    
    def import_state(self, filename: str = "filesystem_state.json") -> bool:
        """Import file system state from JSON."""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            # Restore inodes
            from filesystem_core import INode
            self.fs_core.inodes.clear()
            for inode_id_str, inode_data in state['inodes'].items():
                inode_id = int(inode_id_str)
                self.fs_core.inodes[inode_id] = INode.from_dict(inode_data)
            
            return True
        except Exception as e:
            print(f"Error importing state: {e}")
            return False
    
    def get_operation_log(self) -> List[dict]:
        """Get operation log."""
        return self.operation_log
