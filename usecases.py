"""
Practical Use Case Examples
Demonstrates real-world scenarios using the File System Recovery & Optimization Tool
"""

from disk_simulator import DiskSimulator
import time


def usecase_1_database_backup_system():
    """
    Use Case 1: Database Backup System
    Create checkpoints before critical database operations
    """
    print("\n" + "="*70)
    print("USE CASE 1: Database Backup System")
    print("="*70)
    
    sim = DiskSimulator(total_blocks=512, block_size=4096)
    
    # Create database structure
    db_dir = sim.create_directory("database")
    
    # Create initial database files
    users_db = sim.create_file("users.db", 4096, db_dir)
    transactions_db = sim.create_file("transactions.db", 8192, db_dir)
    
    print("\n→ Initial database created")
    print(f"  Users DB: {users_db}")
    print(f"  Transactions DB: {transactions_db}")
    
    # Write initial data
    sim.write_file(users_db, b"User1,User2,User3" * 10)
    sim.write_file(transactions_db, b"TXN001,TXN002" * 20)
    
    # Create checkpoint before critical operation
    checkpoint1 = sim.checkpoint("Pre-backup: Initial database state")
    print(f"\n✓ Checkpoint {checkpoint1}: Initial state backed up")
    
    # Simulate daily updates
    print("\n→ Processing daily transactions...")
    for day in range(1, 4):
        sim.write_file(transactions_db, f"Day{day}_TXN".encode() * 5)
        
        if day % 2 == 0:
            # Create checkpoint after significant updates
            cp = sim.checkpoint(f"End of day {day}")
            print(f"✓ Checkpoint {cp}: Day {day} complete")
    
    # Disaster strikes
    print("\n→ DISASTER: System crash detected!")
    damage = sim.simulate_crash('moderate')
    print(f"✗ {len(damage['damaged_blocks'])} blocks damaged")
    
    # Recovery to specific point in time
    print(f"\n→ Recovering to checkpoint {checkpoint1}...")
    sim.recover_from_crash(checkpoint1)
    print(f"✓ Database recovered to initial state")
    
    # Verify data integrity
    recovered_users = sim.read_file(users_db)
    print(f"\n✓ Recovered users data verified: {len(recovered_users)} bytes")


def usecase_2_log_file_optimization():
    """
    Use Case 2: Log File System Optimization
    Manage system logs with performance optimization
    """
    print("\n" + "="*70)
    print("USE CASE 2: Log File System Optimization")
    print("="*70)
    
    sim = DiskSimulator(total_blocks=512, block_size=4096)
    
    # Create system directories
    logs_dir = sim.create_directory("var")
    logs_subdir = sim.create_directory("log", logs_dir)
    
    print("\n→ Creating system log files...")
    
    # Create various log files
    system_log = sim.create_file("system.log", 2048, logs_subdir)
    app_log = sim.create_file("application.log", 3072, logs_subdir)
    error_log = sim.create_file("error.log", 1024, logs_subdir)
    
    # Simulate continuous logging (high read/write operations)
    log_messages = [
        b"[INFO] System started",
        b"[DEBUG] Process created",
        b"[INFO] Connection established",
        b"[WARN] Memory usage high",
        b"[ERROR] Connection timeout"
    ]
    
    print("→ Simulating continuous logging (100 operations)...")
    for i in range(100):
        msg = log_messages[i % len(log_messages)]
        if i % 3 == 0:
            sim.write_file(system_log, msg)
        elif i % 3 == 1:
            sim.write_file(app_log, msg)
        else:
            sim.write_file(error_log, msg)
        
        # Frequently read system log
        sim.read_file(system_log)
    
    print("✓ Logging simulation complete")
    
    # Analyze performance
    cache_stats = sim.file_access_optimizer.get_cache_stats()
    print(f"\n→ Performance Analysis:")
    print(f"  Cache hit rate: {cache_stats['hit_rate']*100:.1f}%")
    print(f"  Avg read time: {cache_stats['avg_read_time_ms']:.2f} ms")
    
    # Analyze access patterns
    patterns = sim.file_access_optimizer.analyze_access_patterns()
    print(f"  Sequential access: {patterns['sequential_accesses']}")
    print(f"  Random access: {patterns['random_accesses']}")
    
    # Optimize
    print(f"\n→ Running optimization...")
    optimization = sim.optimize()
    print(f"✓ Optimization complete")
    print(f"  Defragmentation gains: {optimization['defragmentation']['gaps_consolidated']} gaps consolidated")
    print(f"  New cache hit rate: {optimization['cache_statistics']['hit_rate']*100:.1f}%")


def usecase_3_media_storage_management():
    """
    Use Case 3: Media Storage Management
    Handle image and video files with recovery
    """
    print("\n" + "="*70)
    print("USE CASE 3: Media Storage Management")
    print("="*70)
    
    sim = DiskSimulator(total_blocks=1024, block_size=4096)
    
    # Create media directories
    media_dir = sim.create_directory("media")
    images_dir = sim.create_directory("images", media_dir)
    videos_dir = sim.create_directory("videos", media_dir)
    backups_dir = sim.create_directory("backups", media_dir)
    
    print("\n→ Creating media library...")
    
    # Create image files
    images = []
    for i in range(5):
        img = sim.create_file(f"photo_{i:02d}.jpg", 2048, images_dir)
        sim.write_file(img, f"Image_{i}".encode() * 50)
        images.append(img)
    
    print(f"✓ Created 5 image files")
    
    # Create video files
    videos = []
    for i in range(3):
        vid = sim.create_file(f"video_{i:02d}.mp4", 8192, videos_dir)
        sim.write_file(vid, f"Video_{i}".encode() * 100)
        videos.append(vid)
    
    print(f"✓ Created 3 video files")
    
    # Create backup checkpoint
    backup_cp = sim.checkpoint("Media library backup")
    print(f"\n✓ Backup checkpoint {backup_cp} created")
    
    # Simulate accidental deletion
    print(f"\n→ User accidentally deletes critical photo...")
    deleted_photo = images[2]
    deleted_photo_id = deleted_photo
    
    stats_before = sim.get_statistics()
    sim.delete_file(deleted_photo_id)
    stats_after = sim.get_statistics()
    
    print(f"✗ Photo deleted")
    print(f"  Free blocks change: {stats_after['filesystem']['free_blocks'] - stats_before['filesystem']['free_blocks']}")
    
    # Check if file is in recovery registry
    if deleted_photo_id in sim.recovery_manager.deleted_files_registry:
        print(f"\n✓ File found in recovery registry")
        
        # Attempt recovery
        if sim.recovery_manager.recover_deleted_file(deleted_photo_id, sim.fs_core):
            print(f"✓ Photo successfully recovered!")
    
    # Alternative: Restore from backup
    print(f"\n→ Alternatively: Restoring from backup checkpoint {backup_cp}...")
    sim.recover_from_crash(backup_cp)
    print(f"✓ Media library restored to backup state")


def usecase_4_system_migration():
    """
    Use Case 4: System File Migration
    Export and import file system during migration
    """
    print("\n" + "="*70)
    print("USE CASE 4: System File Migration")
    print("="*70)
    
    sim1 = DiskSimulator(total_blocks=512, block_size=4096)
    
    # Create source file structure
    print("\n→ Source system: Creating file structure...")
    home_dir = sim1.create_directory("home")
    docs_dir = sim1.create_directory("documents", home_dir)
    
    # Create files
    files = []
    for i in range(3):
        f = sim1.create_file(f"doc_{i}.txt", 2048, docs_dir)
        sim1.write_file(f, f"Document {i} content".encode() * 10)
        files.append(f)
    
    print(f"✓ Source system: 3 documents created")
    
    # Export system state
    print(f"\n→ Exporting system state...")
    export_file = "migration.json"
    sim1.export_state(export_file)
    print(f"✓ System state exported to {export_file}")
    
    # Simulate migration delay...
    stat_before = sim1.get_statistics()
    print(f"\nSource statistics:")
    print(f"  Used blocks: {stat_before['filesystem']['allocated_blocks']}")
    print(f"  Free blocks: {stat_before['filesystem']['free_blocks']}")
    
    # Create target system and import
    print(f"\n→ Target system: Creating new file system...")
    sim2 = DiskSimulator(total_blocks=512, block_size=4096)
    
    print(f"→ Importing system state...")
    sim2.import_state(export_file)
    print(f"✓ System state imported successfully")
    
    # Verify migration
    stat_after = sim2.get_statistics()
    print(f"\nTarget statistics:")
    print(f"  Used blocks: {stat_after['filesystem']['allocated_blocks']}")
    print(f"  Free blocks: {stat_after['filesystem']['free_blocks']}")
    
    print(f"\n✓ Migration complete - System successfully transferred")


def usecase_5_data_recovery_after_fragment():
    """
    Use Case 5: Data Recovery After Severe Fragmentation
    Recover data from highly fragmented file system
    """
    print("\n" + "="*70)
    print("USE CASE 5: Data Recovery After Severe Fragmentation")
    print("="*70)
    
    sim = DiskSimulator(total_blocks=256, block_size=4096)
    fsm = sim.free_space_manager
    
    print("\n→ Creating fragmented file system...")
    
    # Create and delete files to create fragmentation
    files_to_keep = []
    files_to_delete = []
    
    # Create 40 small files
    for i in range(40):
        f = sim.create_file(f"temp_{i}.tmp", 512)
        if i % 3 == 0:
            files_to_keep.append(f)
        else:
            files_to_delete.append(f)
    
    # Delete alternating files
    for f in files_to_delete:
        sim.delete_file(f)
    
    space_before = fsm.get_free_space_info()
    print(f"\n✓ File system fragmented")
    print(f"  Fragmentation gaps: {space_before['num_gaps']}")
    print(f"  Fragmentation ratio: {space_before['fragmentation_ratio']:.2f}")
    print(f"  Largest gap: {space_before['largest_gap']} blocks")
    
    # Important file
    critical_file = sim.create_file("critical_data.bin", 4096)
    sim.write_file(critical_file, b"CRITICAL DATA - MUST RECOVER" * 50)
    print(f"\n✓ Critical file created: {critical_file}")
    
    # Create recovery checkpoint
    recovery_cp = sim.checkpoint("Pre-crash: Critical data backed up")
    print(f"✓ Recovery checkpoint {recovery_cp} created")
    
    # Simulate crash in fragmented system
    print(f"\n→ Simulating crash in fragmented system...")
    damage = sim.simulate_crash('severe')
    print(f"✗ CRASH: {len(damage['damaged_blocks'])} blocks damaged")
    
    # Check integrity
    print(f"\n→ Checking integrity...")
    integrity = sim.check_integrity()
    print(f"  Issues detected: {integrity['total_issues']}")
    
    # Repair
    print(f"→ Repairing file system...")
    repair = sim.repair()
    print(f"✓ Repair complete: {repair['issues_repaired']} issues fixed")
    
    # Try to recover from checkpoint
    print(f"\n→ Attempting recovery from checkpoint {recovery_cp}...")
    if sim.recover_from_crash(recovery_cp):
        recovered_data = sim.read_file(critical_file)
        print(f"✓ Critical file recovered: {len(recovered_data)} bytes")
    
    # Defragment to prevent future issues
    print(f"\n→ Defragmenting system for optimization...")
    defrag_result = sim.free_space_manager.defragment()
    print(f"✓ Defragmentation complete")
    print(f"  Gaps consolidated: {defrag_result['gaps_consolidated']}")
    
    space_after = defrag_result['after']
    print(f"  New fragmentation ratio: {space_after['fragmentation_ratio']:.2f}")


def usecase_6_performance_tuning():
    """
    Use Case 6: Performance Tuning
    Optimize file system performance through strategy selection
    """
    print("\n" + "="*70)
    print("USE CASE 6: Performance Tuning & Allocation Strategy")
    print("="*70)
    
    strategies = ['first_fit', 'best_fit', 'worst_fit']
    results = {}
    
    for strategy in strategies:
        print(f"\n→ Testing with '{strategy}' strategy...")
        
        sim = DiskSimulator(total_blocks=256, block_size=4096)
        fsm = sim.free_space_manager
        fsm.set_allocation_strategy(strategy)
        
        # Create many files
        for i in range(20):
            f = sim.create_file(f"file_{i}.dat", 768)
            sim.write_file(f, b"Data" * 100)
            
            if i % 2 == 1:
                sim.read_file(f)
        
        # Delete some files
        for i in range(0, 20, 2):
            sim.delete_file(i + 1)  # Approximate inode IDs
        
        # Get performance metrics
        stats = sim.get_statistics()
        space_info = fsm.get_free_space_info()
        cache_info = stats['cache']
        
        results[strategy] = {
            'fragmentation': space_info['fragmentation_ratio'],
            'gaps': space_info['num_gaps'],
            'cache_hit_rate': cache_info['hit_rate'] * 100,
            'largest_gap': space_info['largest_gap']
        }
        
        print(f"  Fragmentation: {results[strategy]['fragmentation']:.2f}")
        print(f"  Gaps: {results[strategy]['gaps']}")
        print(f"  Cache hit rate: {results[strategy]['cache_hit_rate']:.1f}%")
    
    # Compare results
    print(f"\n" + "="*70)
    print("STRATEGY COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n{'Strategy':<12} {'Fragmentation':<15} {'Gaps':<8} {'Cache%':<10}")
    print("-" * 50)
    for strategy, metrics in results.items():
        print(f"{strategy:<12} {metrics['fragmentation']:<15.2f} {metrics['gaps']:<8} {metrics['cache_hit_rate']:<10.1f}")
    
    best_strategy = min(results.items(), key=lambda x: x[1]['fragmentation'])
    print(f"\n✓ Recommended strategy: '{best_strategy[0]}' (lowest fragmentation)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PRACTICAL USE CASE EXAMPLES")
    print("File System Recovery & Optimization Tool")
    print("="*70)
    
    try:
        usecase_1_database_backup_system()
        usecase_2_log_file_optimization()
        usecase_3_media_storage_management()
        usecase_4_system_migration()
        usecase_5_data_recovery_after_fragment()
        usecase_6_performance_tuning()
        
        print("\n" + "="*70)
        print("ALL USE CASES COMPLETED SUCCESSFULLY ✓")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
