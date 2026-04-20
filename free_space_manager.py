"""
Free space management using bitmap allocation strategy.
Handles allocation and deallocation of disk blocks.
"""

from typing import List, Optional


class FreeSpaceManager:
    """Manages free space in the file system using bitmap."""
    
    def __init__(self, total_blocks: int):
        """Initialize free space manager with bitmap."""
        self.total_blocks = total_blocks
        self.bitmap = [False] * total_blocks  # False = free, True = allocated
        self.allocation_strategies = ['first_fit', 'best_fit', 'worst_fit']
        self.current_strategy = 'best_fit'
    
    def allocate_blocks(self, num_blocks: int) -> Optional[List[int]]:
        """Allocate contiguous or non-contiguous blocks."""
        allocated_blocks = []
        
        if self.current_strategy == 'first_fit':
            allocated_blocks = self._first_fit(num_blocks)
        elif self.current_strategy == 'best_fit':
            allocated_blocks = self._best_fit(num_blocks)
        elif self.current_strategy == 'worst_fit':
            allocated_blocks = self._worst_fit(num_blocks)
        
        return allocated_blocks if allocated_blocks else None
    
    def _first_fit(self, num_blocks: int) -> List[int]:
        """First Fit: allocate first available space."""
        allocated = []
        gap_start = None
        gap_size = 0
        
        for i in range(self.total_blocks):
            if not self.bitmap[i]:
                if gap_start is None:
                    gap_start = i
                gap_size += 1
                
                if gap_size >= num_blocks:
                    for j in range(gap_start, gap_start + num_blocks):
                        self.bitmap[j] = True
                        allocated.append(j)
                    return allocated
            else:
                gap_start = None
                gap_size = 0
        
        return []
    
    def _best_fit(self, num_blocks: int) -> List[int]:
        """Best Fit: allocate smallest sufficient space."""
        gaps = self._find_gaps()
        suitable_gaps = [
            (start, size) for start, size in gaps if size >= num_blocks
        ]
        
        if not suitable_gaps:
            return []
        
        best_gap = min(suitable_gaps, key=lambda x: x[1])
        allocated = []
        for j in range(best_gap[0], best_gap[0] + num_blocks):
            self.bitmap[j] = True
            allocated.append(j)
        
        return allocated
    
    def _worst_fit(self, num_blocks: int) -> List[int]:
        """Worst Fit: allocate largest available space."""
        gaps = self._find_gaps()
        suitable_gaps = [
            (start, size) for start, size in gaps if size >= num_blocks
        ]
        
        if not suitable_gaps:
            return []
        
        worst_gap = max(suitable_gaps, key=lambda x: x[1])
        allocated = []
        for j in range(worst_gap[0], worst_gap[0] + num_blocks):
            self.bitmap[j] = True
            allocated.append(j)
        
        return allocated
    
    def _find_gaps(self) -> List[tuple]:
        """Find all free space gaps (start, size)."""
        gaps = []
        gap_start = None
        gap_size = 0
        
        for i in range(self.total_blocks):
            if not self.bitmap[i]:
                if gap_start is None:
                    gap_start = i
                gap_size += 1
            else:
                if gap_start is not None:
                    gaps.append((gap_start, gap_size))
                gap_start = None
                gap_size = 0
        
        if gap_start is not None:
            gaps.append((gap_start, gap_size))
        
        return gaps
    
    def deallocate_blocks(self, block_ids: List[int]) -> bool:
        """Deallocate blocks."""
        try:
            for block_id in block_ids:
                if 0 <= block_id < self.total_blocks:
                    self.bitmap[block_id] = False
            return True
        except Exception:
            return False
    
    def is_block_free(self, block_id: int) -> bool:
        """Check if block is free."""
        if 0 <= block_id < self.total_blocks:
            return not self.bitmap[block_id]
        return False
    
    def get_free_space_info(self) -> dict:
        """Get free space statistics."""
        free_blocks = sum(1 for b in self.bitmap if not b)
        allocated_blocks = self.total_blocks - free_blocks
        gaps = self._find_gaps()
        
        return {
            'total_blocks': self.total_blocks,
            'allocated_blocks': allocated_blocks,
            'free_blocks': free_blocks,
            'fragmentation_ratio': allocated_blocks / self.total_blocks if self.total_blocks > 0 else 0,
            'num_gaps': len(gaps),
            'largest_gap': max([g[1] for g in gaps]) if gaps else 0,
            'smallest_gap': min([g[1] for g in gaps]) if gaps else 0,
            'largest_gap_blocks': max([g[1] for g in gaps]) if gaps else 0
        }
    
    def defragment(self) -> dict:
        """Perform defragmentation to consolidate free space."""
        gaps_before = self._find_gaps()
        before_info = self.get_free_space_info()
        
        # Simulate defragmentation by reorganizing blocks
        defrag_blocks = []
        for i, allocated in enumerate(self.bitmap):
            if allocated:
                defrag_blocks.append(i)
        
        # Reset and reallocate from beginning
        self.bitmap = [False] * self.total_blocks
        for i, block_id in enumerate(defrag_blocks):
            self.bitmap[i] = True
        
        after_info = self.get_free_space_info()
        
        return {
            'before': before_info,
            'after': after_info,
            'gaps_consolidated': len(gaps_before) - after_info['num_gaps']
        }
    
    def set_allocation_strategy(self, strategy: str) -> bool:
        """Change allocation strategy."""
        if strategy in self.allocation_strategies:
            self.current_strategy = strategy
            return True
        return False
