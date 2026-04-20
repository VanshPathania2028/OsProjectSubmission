"""
Recovery manager for handling disk crashes and file system corruption.
Implements recovery techniques and data restoration.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


class RecoveryPoint:
    """Represents a recovery checkpoint."""
    
    def __init__(self, checkpoint_id: int, timestamp: float, description: str):
        self.checkpoint_id = checkpoint_id
        self.timestamp = timestamp
        self.description = description
        self.filesystem_state = {}  # Serialized state
        self.inode_backup = {}
        self.block_map_backup = {}
        self.block_backup = {}


class RecoveryManager:
    """Manages file system recovery and restoration."""
    
    def __init__(self):
        """Initialize recovery manager."""
        self.recovery_points: Dict[int, RecoveryPoint] = {}
        self.checkpoint_counter = 0
        self.recovery_log: List[dict] = []
        self.corruption_detected = []
        self.deleted_files_registry: Dict[int, dict] = {}  # inode_id -> file_metadata
    
    def create_checkpoint(self, fs_core, description: str = "Manual checkpoint") -> Optional[int]:
        """Create a recovery checkpoint."""
        timestamp = datetime.now().timestamp()
        checkpoint = RecoveryPoint(
            self.checkpoint_counter,
            timestamp,
            description
        )
        
        # Backup filesystem state
        checkpoint.inode_backup = {
            inode_id: inode.to_dict()
            for inode_id, inode in fs_core.inodes.items()
        }
        
        checkpoint.block_map_backup = {
            block_id: block.is_allocated
            for block_id, block in fs_core.blocks.items()
        }

        checkpoint.block_backup = {
            block_id: {
                'data': bytes(block.data),
                'checksum': block.checksum,
                'is_allocated': block.is_allocated
            }
            for block_id, block in fs_core.blocks.items()
        }
        
        self.recovery_points[self.checkpoint_counter] = checkpoint
        self.checkpoint_counter += 1
        
        self.recovery_log.append({
            'timestamp': timestamp,
            'action': 'checkpoint_created',
            'checkpoint_id': checkpoint.checkpoint_id
        })
        
        return checkpoint.checkpoint_id
    
    def detect_corruption(self, fs_core) -> List[dict]:
        """Detect file system corruption."""
        issues = []
        
        # Check for orphaned inodes
        for inode_id, inode in fs_core.inodes.items():
            if inode.parent_inode is not None:
                parent = fs_core.get_inode(inode.parent_inode)
                if not parent:
                    issues.append({
                        'type': 'orphaned_inode',
                        'inode_id': inode_id,
                        'filename': inode.filename,
                        'severity': 'high'
                    })
        
        # Check for circular directory references
        visited = set()
        for inode_id in fs_core.inodes:
            if self._detect_cycle(inode_id, fs_core, set()):
                issues.append({
                    'type': 'circular_reference',
                    'inode_id': inode_id,
                    'severity': 'high'
                })
        
        # Check block checksums
        for block_id, block in fs_core.blocks.items():
            if block.is_allocated:
                calculated_checksum = block.calculate_checksum()
                if calculated_checksum != block.checksum:
                    issues.append({
                        'type': 'checksum_mismatch',
                        'block_id': block_id,
                        'severity': 'high'
                    })
        
        self.corruption_detected = issues
        return issues
    
    def _detect_cycle(self, inode_id: int, fs_core, visited: set) -> bool:
        """Detect cyclic references in directory structure."""
        if inode_id in visited:
            return True
        
        visited.add(inode_id)
        inode = fs_core.get_inode(inode_id)
        
        if inode and inode.is_directory:
            for child_inode_id in inode.directory_entries.values():
                if self._detect_cycle(child_inode_id, fs_core, visited.copy()):
                    return True
        
        return False
    
    def recover_from_checkpoint(self, checkpoint_id: int, fs_core) -> bool:
        """Recover file system from a checkpoint."""
        if checkpoint_id not in self.recovery_points:
            return False
        
        checkpoint = self.recovery_points[checkpoint_id]
        
        # Restore inodes
        fs_core.inodes.clear()
        for inode_id, inode_data in checkpoint.inode_backup.items():
            from filesystem_core import INode
            fs_core.inodes[inode_id] = INode.from_dict(inode_data)
        
        # Restore block map
        for block_id, is_allocated in checkpoint.block_map_backup.items():
            if block_id < len(fs_core.blocks):
                fs_core.blocks[block_id].is_allocated = is_allocated

        # Restore block contents and checksums
        for block_id, block_data in checkpoint.block_backup.items():
            if block_id < len(fs_core.blocks):
                fs_core.blocks[block_id].data = bytearray(block_data['data'])
                fs_core.blocks[block_id].checksum = block_data['checksum']
                fs_core.blocks[block_id].is_allocated = block_data['is_allocated']
        
        self.recovery_log.append({
            'timestamp': datetime.now().timestamp(),
            'action': 'checkpoint_restored',
            'checkpoint_id': checkpoint_id
        })
        
        return True
    
    def register_deleted_file(self, inode_id: int, filename: str,
                             file_size: int, block_pointers: List[int],
                             parent_inode: Optional[int] = None):
        """Register a deleted file for potential recovery."""
        self.deleted_files_registry[inode_id] = {
            'filename': filename,
            'file_size': file_size,
            'block_pointers': block_pointers,
            'parent_inode': parent_inode,
            'deleted_time': datetime.now().timestamp()
        }
    
    def recover_deleted_file(self, inode_id: int, fs_core) -> bool:
        """Attempt to recover a deleted file."""
        if inode_id not in self.deleted_files_registry:
            return False
        
        file_info = self.deleted_files_registry[inode_id]
        
        inode = fs_core.get_inode(inode_id)
        if inode is None:
            return False

        inode.filename = file_info['filename']
        inode.file_size = file_info['file_size']
        inode.block_pointers = file_info['block_pointers']
        inode.parent_inode = file_info.get('parent_inode')
        inode.is_allocated = True

        for block_id in inode.block_pointers:
            if block_id in fs_core.blocks:
                fs_core.blocks[block_id].is_allocated = True

        parent_inode_id = file_info.get('parent_inode')
        if parent_inode_id is not None:
            parent = fs_core.get_inode(parent_inode_id)
            if parent and parent.is_directory:
                parent.directory_entries[inode.filename] = inode_id
        
        self.recovery_log.append({
            'timestamp': datetime.now().timestamp(),
            'action': 'file_recovered',
            'inode_id': inode_id,
            'filename': file_info['filename']
        })
        
        return True
    
    def simulate_disk_crash(self, fs_core, severity: str = 'moderate') -> dict:
        """Simulate a disk crash with varying severity."""
        damage_report = {
            'severity': severity,
            'timestamp': datetime.now().timestamp(),
            'damaged_blocks': [],
            'corrupted_inodes': [],
            'recovery_recommendation': ''
        }
        
        import random
        
        if severity == 'light':
            # Damage 5-10% of blocks
            num_damaged = random.randint(
                int(len(fs_core.blocks) * 0.05),
                int(len(fs_core.blocks) * 0.10)
            )
            recovery_recommendation = 'Use incremental recovery from latest checkpoint'
        
        elif severity == 'moderate':
            # Damage 20-40% of blocks
            num_damaged = random.randint(
                int(len(fs_core.blocks) * 0.20),
                int(len(fs_core.blocks) * 0.40)
            )
            recovery_recommendation = 'Full file system recovery recommended'
        
        else:  # severe
            # Damage 50%+ of blocks
            num_damaged = random.randint(
                int(len(fs_core.blocks) * 0.50),
                int(len(fs_core.blocks) * 0.80)
            )
            recovery_recommendation = 'Critical damage - restore from backup'
        
        allocated_blocks = [
            block_id for block_id, block in fs_core.blocks.items()
            if block.is_allocated
        ]
        candidate_blocks = allocated_blocks if allocated_blocks else list(fs_core.blocks.keys())
        
        # Simulate damage, preferring allocated blocks so integrity checks surface real issues.
        damaged_blocks = random.sample(
            candidate_blocks,
            min(num_damaged, len(candidate_blocks))
        )
        
        for block_id in damaged_blocks:
            if block_id < len(fs_core.blocks):
                block = fs_core.blocks[block_id]
                if block.data:
                    corrupted = bytearray(block.data)
                    corrupted[0] = (corrupted[0] + 1) % 256
                    block.data = corrupted
                else:
                    block.data = bytearray(b'\x01')
                # Leave checksum stale so detect_corruption can identify the mismatch.
                damage_report['damaged_blocks'].append(block_id)
        
        damage_report['recovery_recommendation'] = recovery_recommendation
        
        self.recovery_log.append({
            'timestamp': datetime.now().timestamp(),
            'action': 'disk_crash_simulated',
            'severity': severity,
            'damage_report': damage_report
        })
        
        return damage_report
    
    def repair_filesystem(self, fs_core) -> dict:
        """Repair damaged file system."""
        repair_report = {
            'timestamp': datetime.now().timestamp(),
            'issues_detected': len(self.corruption_detected),
            'issues_repaired': 0,
            'actions_taken': []
        }
        
        # Repair orphaned inodes
        orphaned = [
            issue for issue in self.corruption_detected
            if issue['type'] == 'orphaned_inode'
        ]
        
        for issue in orphaned:
            # Move to lost+found directory
            fs_core.deallocate_inode(issue['inode_id'])
            repair_report['issues_repaired'] += 1
            repair_report['actions_taken'].append(
                f"Removed orphaned inode {issue['inode_id']}"
            )
        
        # Repair block checksums
        checksum_issues = [
            issue for issue in self.corruption_detected
            if issue['type'] == 'checksum_mismatch'
        ]
        
        for block_id in range(len(fs_core.blocks)):
            if block_id < len(fs_core.blocks):
                fs_core.blocks[block_id].checksum = \
                    fs_core.blocks[block_id].calculate_checksum()
        
        repair_report['issues_repaired'] += len(checksum_issues)
        
        self.recovery_log.append({
            'timestamp': datetime.now().timestamp(),
            'action': 'filesystem_repaired',
            'report': repair_report
        })
        
        return repair_report
    
    def get_recovery_history(self) -> List[dict]:
        """Get recovery operation history."""
        return self.recovery_log
