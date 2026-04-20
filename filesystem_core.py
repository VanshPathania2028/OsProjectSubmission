"""
Core file system data structures and operations.
Provides the foundation for file and directory management.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class INode:
    """Represents an inode (file metadata) in the file system."""
    inode_id: int
    filename: str
    file_size: int
    created_time: float
    modified_time: float
    accessed_time: float
    permissions: str = "rw-r--r--"
    owner: str = "root"
    block_pointers: List[int] = field(default_factory=list)
    is_directory: bool = False
    parent_inode: Optional[int] = None
    directory_entries: Dict[str, int] = field(default_factory=dict)  # name -> inode_id
    is_allocated: bool = True
    
    def to_dict(self) -> dict:
        """Convert inode to dictionary for serialization."""
        return {
            'inode_id': self.inode_id,
            'filename': self.filename,
            'file_size': self.file_size,
            'created_time': self.created_time,
            'modified_time': self.modified_time,
            'accessed_time': self.accessed_time,
            'permissions': self.permissions,
            'owner': self.owner,
            'block_pointers': self.block_pointers,
            'is_directory': self.is_directory,
            'parent_inode': self.parent_inode,
            'directory_entries': self.directory_entries,
            'is_allocated': self.is_allocated
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'INode':
        """Reconstruct inode from dictionary."""
        return INode(
            inode_id=data['inode_id'],
            filename=data['filename'],
            file_size=data['file_size'],
            created_time=data['created_time'],
            modified_time=data['modified_time'],
            accessed_time=data['accessed_time'],
            permissions=data.get('permissions', 'rw-r--r--'),
            owner=data.get('owner', 'root'),
            block_pointers=data.get('block_pointers', []),
            is_directory=data.get('is_directory', False),
            parent_inode=data.get('parent_inode'),
            directory_entries=data.get('directory_entries', {}),
            is_allocated=data.get('is_allocated', True)
        )


@dataclass
class Block:
    """Represents a disk block."""
    block_id: int
    data: bytearray
    is_allocated: bool = False
    checksum: int = 0
    
    def calculate_checksum(self) -> int:
        """Calculate checksum for data integrity."""
        return sum(self.data) % 256 if self.data else 0


class FileSystemCore:
    """Core file system manager."""
    
    def __init__(self, total_blocks: int = 1024, block_size: int = 4096):
        """Initialize file system."""
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.blocks: Dict[int, Block] = {
            i: Block(i, bytearray(block_size)) 
            for i in range(total_blocks)
        }
        self.inodes: Dict[int, INode] = {}
        self.inode_counter = 0
        self.root_inode: Optional[INode] = None
        self._initialize_root()
    
    def _initialize_root(self):
        """Initialize root directory inode."""
        current_time = datetime.now().timestamp()
        self.root_inode = INode(
            inode_id=0,
            filename="/",
            file_size=0,
            created_time=current_time,
            modified_time=current_time,
            accessed_time=current_time,
            is_directory=True,
            parent_inode=None
        )
        self.inodes[0] = self.root_inode
        self.inode_counter = 1
    
    def allocate_inode(self, filename: str, is_directory: bool = False, 
                      parent_inode_id: int = 0) -> Optional[INode]:
        """Allocate a new inode."""
        current_time = datetime.now().timestamp()
        inode = INode(
            inode_id=self.inode_counter,
            filename=filename,
            file_size=0,
            created_time=current_time,
            modified_time=current_time,
            accessed_time=current_time,
            is_directory=is_directory,
            parent_inode=parent_inode_id
        )
        self.inodes[self.inode_counter] = inode
        self.inode_counter += 1
        return inode
    
    def deallocate_inode(self, inode_id: int):
        """Mark inode as deleted."""
        if inode_id in self.inodes:
            self.inodes[inode_id].is_allocated = False
    
    def get_inode(self, inode_id: int) -> Optional[INode]:
        """Retrieve an inode."""
        return self.inodes.get(inode_id)
    
    def write_block(self, block_id: int, data: bytes) -> bool:
        """Write data to a block."""
        if block_id >= self.total_blocks:
            return False
        self.blocks[block_id].data = bytearray(data[:self.block_size])
        self.blocks[block_id].checksum = self.blocks[block_id].calculate_checksum()
        return True
    
    def read_block(self, block_id: int) -> Optional[bytes]:
        """Read data from a block."""
        if block_id >= self.total_blocks:
            return None
        return bytes(self.blocks[block_id].data)
    
    def get_system_info(self) -> dict:
        """Get file system information."""
        allocated_blocks = sum(1 for b in self.blocks.values() if b.is_allocated)
        allocated_inodes = sum(1 for i in self.inodes.values() if i.is_allocated)
        
        return {
            'total_blocks': self.total_blocks,
            'allocated_blocks': allocated_blocks,
            'free_blocks': self.total_blocks - allocated_blocks,
            'block_size': self.block_size,
            'total_inodes': len(self.inodes),
            'allocated_inodes': allocated_inodes,
            'total_capacity_mb': (self.total_blocks * self.block_size) / (1024 * 1024)
        }
