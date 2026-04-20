"""
Directory management for hierarchical file system organization.
Handles directory creation, navigation, and file organization.
"""

from typing import Optional, List, Tuple
from filesystem_core import FileSystemCore, INode


class DirectoryManager:
    """Manages directory structure and operations."""
    
    def __init__(self, fs_core: FileSystemCore):
        """Initialize directory manager."""
        self.fs_core = fs_core
        self.current_dir_id = 0  # Root directory
    
    def create_directory(self, dir_name: str, parent_dir_id: int = None) -> Optional[INode]:
        """Create a new directory."""
        if parent_dir_id is None:
            parent_dir_id = self.current_dir_id
        
        # Check if parent exists
        parent_dir = self.fs_core.get_inode(parent_dir_id)
        if not parent_dir or not parent_dir.is_directory:
            return None
        
        # Check if name already exists
        if dir_name in parent_dir.directory_entries:
            return None
        
        # Allocate new inode for directory
        new_dir = self.fs_core.allocate_inode(
            dir_name,
            is_directory=True,
            parent_inode_id=parent_dir_id
        )
        
        # Add to parent directory
        parent_dir.directory_entries[dir_name] = new_dir.inode_id
        
        return new_dir
    
    def delete_directory(self, dir_id: int) -> bool:
        """Delete an empty directory."""
        dir_inode = self.fs_core.get_inode(dir_id)
        
        if not dir_inode or not dir_inode.is_directory:
            return False
        
        # Check if directory is empty
        if dir_inode.directory_entries:
            return False
        
        # Remove from parent
        if dir_inode.parent_inode is not None:
            parent = self.fs_core.get_inode(dir_inode.parent_inode)
            if parent:
                for name, inode_id in parent.directory_entries.items():
                    if inode_id == dir_id:
                        del parent.directory_entries[name]
                        break
        
        self.fs_core.deallocate_inode(dir_id)
        return True
    
    def create_file(self, filename: str, file_size: int, 
                   parent_dir_id: int = None) -> Optional[INode]:
        """Create a new file."""
        if parent_dir_id is None:
            parent_dir_id = self.current_dir_id
        
        parent_dir = self.fs_core.get_inode(parent_dir_id)
        if not parent_dir or not parent_dir.is_directory:
            return None
        
        # Check if name already exists
        if filename in parent_dir.directory_entries:
            return None
        
        # Allocate new inode for file
        new_file = self.fs_core.allocate_inode(
            filename,
            is_directory=False,
            parent_inode_id=parent_dir_id
        )
        new_file.file_size = file_size
        
        # Add to parent directory
        parent_dir.directory_entries[filename] = new_file.inode_id
        
        return new_file
    
    def delete_file(self, file_id: int) -> bool:
        """Delete a file."""
        file_inode = self.fs_core.get_inode(file_id)
        
        if not file_inode or file_inode.is_directory:
            return False
        
        # Remove from parent directory
        if file_inode.parent_inode is not None:
            parent = self.fs_core.get_inode(file_inode.parent_inode)
            if parent:
                for name, inode_id in parent.directory_entries.items():
                    if inode_id == file_id:
                        del parent.directory_entries[name]
                        break
        
        self.fs_core.deallocate_inode(file_id)
        return True
    
    def change_directory(self, dir_id: int) -> bool:
        """Change current directory."""
        dir_inode = self.fs_core.get_inode(dir_id)
        if dir_inode and dir_inode.is_directory:
            self.current_dir_id = dir_id
            return True
        return False
    
    def list_directory(self, dir_id: int = None) -> List[dict]:
        """List contents of a directory."""
        if dir_id is None:
            dir_id = self.current_dir_id
        
        dir_inode = self.fs_core.get_inode(dir_id)
        if not dir_inode or not dir_inode.is_directory:
            return []
        
        contents = []
        for name, inode_id in dir_inode.directory_entries.items():
            inode = self.fs_core.get_inode(inode_id)
            if inode:
                contents.append({
                    'name': name,
                    'inode_id': inode_id,
                    'type': 'directory' if inode.is_directory else 'file',
                    'size': inode.file_size,
                    'modified': inode.modified_time
                })
        
        return contents
    
    def find_file(self, filename: str, search_dir: int = None) -> Optional[int]:
        """Search for a file recursively."""
        if search_dir is None:
            search_dir = self.current_dir_id
        
        dir_inode = self.fs_core.get_inode(search_dir)
        if not dir_inode or not dir_inode.is_directory:
            return None
        
        # Check current directory
        if filename in dir_inode.directory_entries:
            return dir_inode.directory_entries[filename]
        
        # Recursive search in subdirectories
        for name, inode_id in dir_inode.directory_entries.items():
            inode = self.fs_core.get_inode(inode_id)
            if inode and inode.is_directory:
                result = self.find_file(filename, inode_id)
                if result is not None:
                    return result
        
        return None
    
    def get_path(self, inode_id: int) -> str:
        """Get full path of an inode."""
        inode = self.fs_core.get_inode(inode_id)
        if not inode:
            return ""
        
        if inode_id == 0:
            return "/"
        
        path_parts = []
        current = inode
        
        while current.parent_inode is not None:
            path_parts.append(current.filename)
            current = self.fs_core.get_inode(current.parent_inode)
        
        path_parts.reverse()
        return "/" + "/".join(path_parts)
    
    def get_directory_stats(self, dir_id: int = None) -> dict:
        """Get statistics about a directory."""
        if dir_id is None:
            dir_id = self.current_dir_id
        
        dir_inode = self.fs_core.get_inode(dir_id)
        if not dir_inode or not dir_inode.is_directory:
            return {}
        
        total_files = 0
        total_dirs = 0
        total_size = 0
        
        for name, inode_id in dir_inode.directory_entries.items():
            inode = self.fs_core.get_inode(inode_id)
            if inode:
                if inode.is_directory:
                    total_dirs += 1
                else:
                    total_files += 1
                    total_size += inode.file_size
        
        return {
            'path': self.get_path(dir_id),
            'total_files': total_files,
            'total_directories': total_dirs,
            'total_size_bytes': total_size,
            'created': dir_inode.created_time,
            'modified': dir_inode.modified_time
        }
