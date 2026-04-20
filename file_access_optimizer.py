"""
File access optimization engine for improving read/write performance.
Handles caching, access pattern analysis, and IO optimization.
"""

from typing import Dict, List, Optional
from collections import deque
import time


class CacheEntry:
    """Represents a cache entry."""
    
    def __init__(self, block_id: int, data: bytes, timestamp: float):
        self.block_id = block_id
        self.data = data
        self.timestamp = timestamp
        self.access_count = 0
        self.last_accessed = timestamp


class FileAccessOptimizer:
    """Optimizes file read/write operations."""
    
    def __init__(self, cache_size: int = 128, block_size: int = 4096):
        """Initialize file access optimizer."""
        self.cache_size = cache_size
        self.block_size = block_size
        self.cache: Dict[int, CacheEntry] = {}
        self.access_log: deque = deque(maxlen=1000)
        self.read_ahead_buffer = {}
        self.optimization_metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'read_operations': 0,
            'write_operations': 0,
            'total_read_time': 0,
            'total_write_time': 0
        }
    
    def read_block(self, block_id: int, filesystem_read_func) -> Optional[bytes]:
        """Read block with caching."""
        start_time = time.time()
        self.optimization_metrics['read_operations'] += 1
        
        # Check cache first
        if block_id in self.cache:
            elapsed = time.time() - start_time
            self.optimization_metrics['cache_hits'] += 1
            self.optimization_metrics['total_read_time'] += elapsed
            self.cache[block_id].access_count += 1
            self.cache[block_id].last_accessed = start_time
            self._log_access('read', block_id, elapsed)
            return self.cache[block_id].data
        
        # Cache miss - read from filesystem
        self.optimization_metrics['cache_misses'] += 1
        data = filesystem_read_func(block_id)
        
        if data:
            # Add to cache
            self._add_to_cache(block_id, data, start_time)
            
            # Predictive read-ahead
            self._read_ahead(block_id, filesystem_read_func)
        
        elapsed = time.time() - start_time
        self.optimization_metrics['total_read_time'] += elapsed
        
        self._log_access('read', block_id, elapsed)
        return data
    
    def write_block(self, block_id: int, data: bytes, 
                    filesystem_write_func, writeback: bool = True) -> bool:
        """Write block with optional writeback cache."""
        start_time = time.time()
        
        # Update cache
        self._add_to_cache(block_id, data, start_time)
        
        # Perform write operation
        if writeback:
            success = filesystem_write_func(block_id, data)
        else:
            success = True  # Will be written later
        
        elapsed = time.time() - start_time
        self.optimization_metrics['write_operations'] += 1
        self.optimization_metrics['total_write_time'] += elapsed
        
        self._log_access('write', block_id, elapsed)
        return success
    
    def _add_to_cache(self, block_id: int, data: bytes, timestamp: float):
        """Add block to cache with eviction if necessary."""
        if len(self.cache) >= self.cache_size:
            # Evict using LRU
            lru_block = min(
                self.cache.items(),
                key=lambda x: x[1].last_accessed
            )[0]
            del self.cache[lru_block]
        
        self.cache[block_id] = CacheEntry(block_id, data, timestamp)
    
    def _read_ahead(self, block_id: int, filesystem_read_func, 
                    lookahead: int = 4):
        """Predictive read-ahead for sequential access patterns."""
        for i in range(1, lookahead + 1):
            next_block = block_id + i
            if next_block not in self.cache:
                try:
                    data = filesystem_read_func(next_block)
                    if data and len(self.cache) < self.cache_size:
                        self._add_to_cache(next_block, data, time.time())
                except:
                    pass
    
    def _log_access(self, operation: str, block_id: int, elapsed: float):
        """Log access pattern."""
        self.access_log.append({
            'operation': operation,
            'block_id': block_id,
            'timestamp': time.time(),
            'elapsed': elapsed
        })
    
    def analyze_access_patterns(self) -> dict:
        """Analyze file access patterns."""
        if not self.access_log:
            return {}
        
        sequential_accesses = 0
        random_accesses = 0
        prev_block = None
        
        for entry in self.access_log:
            block_id = entry['block_id']
            if prev_block is not None:
                if block_id == prev_block + 1:
                    sequential_accesses += 1
                else:
                    random_accesses += 1
            prev_block = block_id
        
        most_accessed = self._get_most_accessed_blocks(5)
        
        return {
            'sequential_accesses': sequential_accesses,
            'random_accesses': random_accesses,
            'sequentiality_ratio': sequential_accesses / (sequential_accesses + random_accesses)
            if (sequential_accesses + random_accesses) > 0 else 0,
            'most_accessed_blocks': most_accessed,
            'total_operations': len(self.access_log)
        }
    
    def _get_most_accessed_blocks(self, limit: int = 5) -> List[dict]:
        """Get most frequently accessed blocks."""
        block_stats = {}
        for block_id, entry in self.cache.items():
            block_stats[block_id] = entry.access_count
        
        sorted_blocks = sorted(
            block_stats.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [{'block_id': b, 'access_count': c} for b, c in sorted_blocks[:limit]]
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total_ops = (self.optimization_metrics['cache_hits'] + 
                    self.optimization_metrics['cache_misses'])
        
        hit_rate = (self.optimization_metrics['cache_hits'] / total_ops 
                   if total_ops > 0 else 0)
        
        avg_read_time = (self.optimization_metrics['total_read_time'] / 
                        self.optimization_metrics['read_operations']
                        if self.optimization_metrics['read_operations'] > 0 else 0)
        
        avg_write_time = (self.optimization_metrics['total_write_time'] / 
                         self.optimization_metrics['write_operations']
                         if self.optimization_metrics['write_operations'] > 0 else 0)
        
        return {
            'cache_hits': self.optimization_metrics['cache_hits'],
            'cache_misses': self.optimization_metrics['cache_misses'],
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'max_cache_size': self.cache_size,
            'read_operations': self.optimization_metrics['read_operations'],
            'write_operations': self.optimization_metrics['write_operations'],
            'avg_read_time_ms': avg_read_time * 1000,
            'avg_write_time_ms': avg_write_time * 1000
        }
    
    def flush_cache(self) -> int:
        """Clear cache."""
        flushed = len(self.cache)
        self.cache.clear()
        return flushed
    
    def optimize_block_placement(self, block_ids: List[int]) -> dict:
        """Optimize placement of frequently accessed blocks."""
        access_freq = {}
        for entry in self.access_log:
            bid = entry['block_id']
            access_freq[bid] = access_freq.get(bid, 0) + 1
        
        hot_blocks = [
            (bid, freq) for bid, freq in access_freq.items() 
            if bid in block_ids
        ]
        hot_blocks.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'hot_blocks': hot_blocks[:10],
            'cold_blocks': hot_blocks[-10:],
            'recommendation': 'Place hot blocks near disk head to reduce seek time'
        }
