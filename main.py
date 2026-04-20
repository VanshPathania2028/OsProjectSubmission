"""
File System Recovery and Optimization Tool
Main application with CLI and demo scenarios.
"""

from disk_simulator import DiskSimulator
import json
from typing import Optional


class FileSystemTool:
    """Interactive file system recovery and optimization tool."""
    
    def __init__(self):
        """Initialize the tool."""
        self.simulator: Optional[DiskSimulator] = None
        self.running = True
    
    def initialize_filesystem(self, total_blocks: int = 1024, 
                             block_size: int = 4096):
        """Initialize a new file system."""
        self.simulator = DiskSimulator(total_blocks, block_size)
        print(f"\n✓ File system initialized with {total_blocks} blocks of {block_size} bytes each")
        print(f"  Total capacity: {(total_blocks * block_size) / (1024*1024):.2f} MB\n")
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "="*60)
        print("FILE SYSTEM RECOVERY & OPTIMIZATION TOOL")
        print("="*60)
        print("\n1. Create File System")
        print("2. File Operations (Create/Delete/Read/Write)")
        print("3. Directory Operations")
        print("4. Create Recovery Checkpoint")
        print("5. Simulate Disk Crash")
        print("6. Check Integrity & Repair")
        print("7. Optimize File System")
        print("8. View Statistics")
        print("9. Demo Scenario")
        print("10. Export/Import State")
        print("11. Exit")
        print("\n" + "="*60)
    
    def file_operations_menu(self):
        """File operations submenu."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        print("\n--- File Operations ---")
        print("1. Create File")
        print("2. Delete File")
        print("3. Write File")
        print("4. Read File")
        print("5. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            filename = input("Enter filename: ").strip()
            size = int(input("Enter file size (bytes): ").strip())
            inode_id = self.simulator.create_file(filename, size)
            if inode_id:
                print(f"✓ File created with inode ID: {inode_id}")
            else:
                print("✗ Failed to create file")
        
        elif choice == '2':
            inode_id = int(input("Enter inode ID to delete: ").strip())
            if self.simulator.delete_file(inode_id):
                print(f"✓ File deleted")
            else:
                print("✗ Failed to delete file")
        
        elif choice == '3':
            inode_id = int(input("Enter inode ID: ").strip())
            data = input("Enter data to write: ").strip().encode()
            if self.simulator.write_file(inode_id, data):
                print("✓ Data written successfully")
            else:
                print("✗ Failed to write")
        
        elif choice == '4':
            inode_id = int(input("Enter inode ID: ").strip())
            data = self.simulator.read_file(inode_id)
            if data:
                print(f"✓ File data: {data.decode(errors='ignore')}")
            else:
                print("✗ Failed to read file")
    
    def directory_operations_menu(self):
        """Directory operations submenu."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        print("\n--- Directory Operations ---")
        print("1. Create Directory")
        print("2. List Directory")
        print("3. Change Directory")
        print("4. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            dirname = input("Enter directory name: ").strip()
            inode_id = self.simulator.create_directory(dirname)
            if inode_id:
                print(f"✓ Directory created with inode ID: {inode_id}")
            else:
                print("✗ Failed to create directory")
        
        elif choice == '2':
            dir_id = int(input("Enter directory inode ID (0 for root): ").strip())
            contents = self.simulator.list_directory(dir_id)
            if contents:
                print("\nDirectory contents:")
                for item in contents:
                    print(f"  - {item['name']} ({item['type']}) - {item['size']} bytes")
            else:
                print("Directory is empty")
        
        elif choice == '3':
            dir_id = int(input("Enter directory inode ID: ").strip())
            if self.simulator.directory_manager.change_directory(dir_id):
                print("✓ Directory changed")
            else:
                print("✗ Invalid directory")
    
    def recovery_operations(self):
        """Recovery and repair operations."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        print("\n--- Recovery & Repair ---")
        print("1. Create Checkpoint")
        print("2. Simulate Crash")
        print("3. Check Integrity")
        print("4. Repair Filesystem")
        print("5. Recover from Checkpoint")
        print("6. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            desc = input("Enter checkpoint description: ").strip()
            checkpoint_id = self.simulator.checkpoint(desc)
            if checkpoint_id is not None:
                print(f"✓ Checkpoint {checkpoint_id} created")
            else:
                print("✗ Failed to create checkpoint")
        
        elif choice == '2':
            print("Crash severity: light, moderate, severe")
            severity = input("Select severity: ").strip()
            damage = self.simulator.simulate_crash(severity)
            print(f"\n✗ DISK CRASH SIMULATED!")
            print(f"  Severity: {damage['severity']}")
            print(f"  Damaged blocks: {len(damage['damaged_blocks'])}")
            print(f"  Recovery: {damage['recovery_recommendation']}")
        
        elif choice == '3':
            integrity = self.simulator.check_integrity()
            print(f"\nFilesystem Status: {'✓ HEALTHY' if integrity['filesystem_healthy'] else '✗ CORRUPTED'}")
            print(f"Total issues found: {integrity['total_issues']}")
            if integrity['issues']:
                print("\nIssues:")
                for issue in integrity['issues']:
                    print(f"  - {issue['type']} (severity: {issue['severity']})")
        
        elif choice == '4':
            result = self.simulator.repair()
            print(f"\n✓ Repair Complete")
            print(f"  Issues detected: {result['issues_detected']}")
            print(f"  Issues repaired: {result['issues_repaired']}")
        
        elif choice == '5':
            checkpoint_id = int(input("Enter checkpoint ID to recover: ").strip())
            if self.simulator.recover_from_crash(checkpoint_id):
                print("✓ Filesystem recovered from checkpoint")
            else:
                print("✗ Recovery failed")
    
    def optimization_menu(self):
        """Optimization operations."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        print("\n--- Optimization ---")
        print("1. Optimize Filesystem")
        print("2. View Cache Statistics")
        print("3. Analyze Access Patterns")
        print("4. Change Allocation Strategy")
        print("5. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            result = self.simulator.optimize()
            print(f"\n✓ Optimization Complete")
            print(f"  Defragmentation: {result['defragmentation']['gaps_consolidated']} gaps consolidated")
            print(f"  Cache Hit Rate: {result['cache_statistics']['hit_rate']*100:.1f}%")
        
        elif choice == '2':
            stats = self.simulator.file_access_optimizer.get_cache_stats()
            print(f"\nCache Statistics:")
            print(f"  Cache Size: {stats['cache_size']}/{stats['max_cache_size']}")
            print(f"  Hit Rate: {stats['hit_rate']*100:.1f}%")
            print(f"  Avg Read Time: {stats['avg_read_time_ms']:.2f} ms")
            print(f"  Avg Write Time: {stats['avg_write_time_ms']:.2f} ms")
        
        elif choice == '3':
            patterns = self.simulator.file_access_optimizer.analyze_access_patterns()
            if patterns:
                print(f"\nAccess Patterns:")
                print(f"  Sequential: {patterns['sequential_accesses']}")
                print(f"  Random: {patterns['random_accesses']}")
                print(f"  Sequentiality: {patterns['sequentiality_ratio']*100:.1f}%")
        
        elif choice == '4':
            strategies = ['first_fit', 'best_fit', 'worst_fit']
            print("Available strategies:", ", ".join(strategies))
            strategy = input("Select strategy: ").strip()
            if self.simulator.free_space_manager.set_allocation_strategy(strategy):
                print(f"✓ Strategy changed to {strategy}")
            else:
                print("✗ Invalid strategy")
    
    def view_statistics(self):
        """View system statistics."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        stats = self.simulator.get_statistics()
        print("\n" + "="*60)
        print("SYSTEM STATISTICS")
        print("="*60)
        
        print(f"\nFilesystem:")
        print(f"  Total blocks: {stats['filesystem']['total_blocks']}")
        print(f"  Allocated blocks: {stats['filesystem']['allocated_blocks']}")
        print(f"  Free blocks: {stats['filesystem']['free_blocks']}")
        print(f"  Total capacity: {stats['filesystem']['total_capacity_mb']:.2f} MB")
        
        print(f"\nFree Space:")
        print(f"  Fragmentation ratio: {stats['free_space']['fragmentation_ratio']:.2f}")
        print(f"  Number of gaps: {stats['free_space']['num_gaps']}")
        print(f"  Largest gap: {stats['free_space']['largest_gap']} blocks")
        
        print(f"\nCache:")
        print(f"  Hit rate: {stats['cache']['hit_rate']*100:.1f}%")
        print(f"  Cache efficiency: {(stats['cache']['cache_hits']/max(1, stats['cache']['cache_hits']+stats['cache']['cache_misses']))*100:.1f}%")
    
    def demo_scenario(self):
        """Run a demo scenario."""
        print("\n--- Demo Scenario ---")
        print("1. Normal Operations Demo")
        print("2. Crash & Recovery Demo")
        print("3. Optimization Demo")
        print("4. Back to Main Menu")
        
        choice = input("Select scenario: ").strip()
        
        if choice == '1':
            self._demo_normal_operations()
        elif choice == '2':
            self._demo_crash_recovery()
        elif choice == '3':
            self._demo_optimization()
    
    def _demo_normal_operations(self):
        """Demo normal file system operations."""
        print("\n→ Initializing file system...")
        self.initialize_filesystem(512, 4096)
        
        print("→ Creating directories...")
        docs_id = self.simulator.create_directory("documents")
        pics_id = self.simulator.create_directory("pictures")
        
        print("→ Creating files...")
        file1 = self.simulator.create_file("readme.txt", 2048, docs_id)
        file2 = self.simulator.create_file("photo.jpg", 8192, pics_id)
        
        print("→ Writing to files...")
        self.simulator.write_file(file1, b"This is a test file content")
        self.simulator.write_file(file2, b"Binary image data here")
        
        print("→ Reading files...")
        data1 = self.simulator.read_file(file1)
        print(f"  Read from readme.txt: {data1[:30]}")
        
        print("\n✓ Demo Complete - File system operational")
    
    def _demo_crash_recovery(self):
        """Demo crash and recovery."""
        print("\n→ Initializing file system...")
        self.initialize_filesystem(256, 4096)
        
        print("→ Creating files...")
        f1 = self.simulator.create_file("important.doc", 4096)
        self.simulator.write_file(f1, b"Important data")
        
        print("→ Creating checkpoint...")
        cp = self.simulator.checkpoint("Pre-crash backup")
        print(f"  Checkpoint {cp} created")
        
        print("\n→ Simulating DISK CRASH...")
        damage = self.simulator.simulate_crash('moderate')
        print(f"  {len(damage['damaged_blocks'])} blocks damaged!")
        
        print("→ Checking filesystem integrity...")
        integrity = self.simulator.check_integrity()
        print(f"  {integrity['total_issues']} corruption issues detected")
        
        print("→ Recovering from checkpoint...")
        self.simulator.recover_from_crash(cp)
        
        print("\n✓ Recovery Complete - Filesystem restored")
    
    def _demo_optimization(self):
        """Demo optimization."""
        print("\n→ Initializing file system...")
        self.initialize_filesystem(256, 4096)
        
        print("→ Creating multiple files...")
        for i in range(10):
            self.simulator.create_file(f"file_{i}.dat", 2048)
        
        print("→ Performing file operations...")
        for _ in range(50):
            self.simulator.read_file(0)
        
        print("→ Optimizing filesystem...")
        result = self.simulator.optimize()
        
        print(f"\nOptimization Results:")
        print(f"  Cache hit rate: {result['cache_statistics']['hit_rate']*100:.1f}%")
        print(f"  Fragmentation gaps consolidated: {result['defragmentation']['gaps_consolidated']}")
        
        print("\n✓ Optimization Complete")
    
    def export_import_menu(self):
        """Export and import menu."""
        if not self.simulator:
            print("Please initialize file system first (Option 1)")
            return
        
        print("\n--- Export/Import ---")
        print("1. Export State")
        print("2. Import State")
        print("3. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            filename = input("Enter filename (default: filesystem_state.json): ").strip()
            if not filename:
                filename = "filesystem_state.json"
            if self.simulator.export_state(filename):
                print(f"✓ State exported to {filename}")
            else:
                print("✗ Export failed")
        
        elif choice == '2':
            filename = input("Enter filename (default: filesystem_state.json): ").strip()
            if not filename:
                filename = "filesystem_state.json"
            if self.simulator.import_state(filename):
                print(f"✓ State imported from {filename}")
            else:
                print("✗ Import failed")
    
    def run(self):
        """Run the main application loop."""
        print("\n" + "="*60)
        print("FILE SYSTEM RECOVERY & OPTIMIZATION TOOL")
        print("="*60)
        
        while self.running:
            self.display_menu()
            choice = input("Select option: ").strip()
            
            if choice == '1':
                blocks = input("Enter total blocks (default 1024): ").strip()
                block_size = input("Enter block size (default 4096): ").strip()
                try:
                    blocks = int(blocks) if blocks else 1024
                    block_size = int(block_size) if block_size else 4096
                    self.initialize_filesystem(blocks, block_size)
                except ValueError:
                    print("Invalid input")
            
            elif choice == '2':
                self.file_operations_menu()
            elif choice == '3':
                self.directory_operations_menu()
            elif choice == '4':
                self.recovery_operations()
            elif choice == '5':
                self.recovery_operations()
            elif choice == '6':
                self.recovery_operations()
            elif choice == '7':
                self.optimization_menu()
            elif choice == '8':
                self.view_statistics()
            elif choice == '9':
                self.demo_scenario()
            elif choice == '10':
                self.export_import_menu()
            elif choice == '11':
                print("\nGoodbye!")
                self.running = False
            else:
                print("Invalid option")


if __name__ == "__main__":
    tool = FileSystemTool()
    tool.run()
