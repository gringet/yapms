#!/usr/bin/env python3
"""
Migration script to convert from pickle-based storage to SQLite-based storage.

Usage:
    python migrate_to_sqlite.py [--pickle-file PATH] [--sqlite-file PATH] [--backup]
"""

import pickle
import sqlite3
import json
import os
import argparse
import shutil
from datetime import datetime
from typing import Dict, List, Any


def load_pickle_data(pickle_path: str) -> Dict[str, Any]:
    """Load data from the pickle file."""
    print(f"Loading data from {pickle_path}...")
    
    if not os.path.exists(pickle_path):
        raise FileNotFoundError(f"Pickle file not found: {pickle_path}")
    
    try:
        with open(pickle_path, "rb") as f:
            data = pickle.load(f)
        print(f"✓ Successfully loaded pickle data")
        return data
    except Exception as e:
        raise Exception(f"Failed to load pickle file: {e}")


def validate_pickle_data(data: Dict[str, Any]) -> bool:
    """Validate that the pickle data has the expected structure."""
    print("Validating pickle data structure...")
    
    if not isinstance(data, dict):
        print("✗ Data is not a dictionary")
        return False
    
    if "tasks" not in data:
        print("✗ Missing 'tasks' key")
        return False
    
    if "kanban" not in data:
        print("✗ Missing 'kanban' key")
        return False
    
    if not isinstance(data["tasks"], dict):
        print("✗ 'tasks' is not a dictionary")
        return False
    
    if not isinstance(data["kanban"], dict):
        print("✗ 'kanban' is not a dictionary")
        return False
    
    print(f"✓ Data structure is valid")
    print(f"  - Found {len(data['tasks'])} tasks")
    print(f"  - Found {len(data['kanban'])} kanban columns")
    
    return True


def create_sqlite_database(sqlite_path: str) -> sqlite3.Connection:
    """Create and initialize the SQLite database."""
    print(f"Creating SQLite database at {sqlite_path}...")
    
    # Check if database already exists
    if os.path.exists(sqlite_path):
        print(f"⚠ Warning: Database file already exists at {sqlite_path}")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            raise Exception("Migration cancelled by user")
        os.remove(sqlite_path)
        print("✓ Removed existing database")
    
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Create kanban table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kanban (
            column_id TEXT PRIMARY KEY,
            ordering TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    print("✓ SQLite database created successfully")
    
    return conn


def migrate_tasks(conn: sqlite3.Connection, tasks: Dict[str, Dict[str, str]]) -> int:
    """Migrate tasks from pickle data to SQLite."""
    print("Migrating tasks...")
    
    cursor = conn.cursor()
    migrated_count = 0
    
    for task_id, task_data in tasks.items():
        try:
            cursor.execute(
                'INSERT INTO tasks (id, title, description) VALUES (?, ?, ?)',
                (
                    task_data.get('id', task_id),
                    task_data.get('title', ''),
                    task_data.get('description', '')
                )
            )
            migrated_count += 1
        except Exception as e:
            print(f"✗ Failed to migrate task {task_id}: {e}")
    
    conn.commit()
    print(f"✓ Migrated {migrated_count}/{len(tasks)} tasks")
    
    return migrated_count


def migrate_kanban(conn: sqlite3.Connection, kanban: Dict[str, List[str]]) -> int:
    """Migrate kanban column orderings from pickle data to SQLite."""
    print("Migrating kanban columns...")
    
    cursor = conn.cursor()
    migrated_count = 0
    
    for column_id, ordering in kanban.items():
        try:
            cursor.execute(
                'INSERT INTO kanban (column_id, ordering) VALUES (?, ?)',
                (column_id, json.dumps(ordering))
            )
            migrated_count += 1
        except Exception as e:
            print(f"✗ Failed to migrate kanban column {column_id}: {e}")
    
    conn.commit()
    print(f"✓ Migrated {migrated_count}/{len(kanban)} kanban columns")
    
    return migrated_count


def verify_migration(conn: sqlite3.Connection, original_data: Dict[str, Any]) -> bool:
    """Verify that the migration was successful."""
    print("Verifying migration...")
    
    cursor = conn.cursor()
    
    # Verify tasks count
    cursor.execute('SELECT COUNT(*) FROM tasks')
    tasks_count = cursor.fetchone()[0]
    expected_tasks = len(original_data['tasks'])
    
    if tasks_count != expected_tasks:
        print(f"✗ Tasks count mismatch: expected {expected_tasks}, got {tasks_count}")
        return False
    
    print(f"✓ Tasks count matches: {tasks_count}")
    
    # Verify kanban columns count
    cursor.execute('SELECT COUNT(*) FROM kanban')
    kanban_count = cursor.fetchone()[0]
    expected_kanban = len(original_data['kanban'])
    
    if kanban_count != expected_kanban:
        print(f"✗ Kanban columns count mismatch: expected {expected_kanban}, got {kanban_count}")
        return False
    
    print(f"✓ Kanban columns count matches: {kanban_count}")
    
    # Verify a sample of data
    cursor.execute('SELECT * FROM tasks LIMIT 1')
    sample_task = cursor.fetchone()
    if sample_task:
        print(f"✓ Sample task verified: {sample_task[0]}")
    
    cursor.execute('SELECT * FROM kanban LIMIT 1')
    sample_kanban = cursor.fetchone()
    if sample_kanban:
        print(f"✓ Sample kanban column verified: {sample_kanban[0]}")
    
    return True


def create_backup(file_path: str) -> str:
    """Create a backup of the original pickle file."""
    if not os.path.exists(file_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    print(f"Creating backup at {backup_path}...")
    shutil.copy2(file_path, backup_path)
    print(f"✓ Backup created successfully")
    
    return backup_path


def main():
    parser = argparse.ArgumentParser(
        description='Migrate data from pickle storage to SQLite database'
    )
    parser.add_argument(
        '--pickle-file',
        default='.data.pkl',
        help='Path to the pickle file (default: .data.pkl)'
    )
    parser.add_argument(
        '--sqlite-file',
        default='.data.db',
        help='Path to the SQLite database file (default: .data.db)'
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create a backup of the pickle file before migration'
    )
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Skip verification after migration'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Data Migration: Pickle → SQLite")
    print("=" * 60)
    print()
    
    try:
        # Create backup if requested
        if args.backup:
            backup_path = create_backup(args.pickle_file)
            if backup_path:
                print()
        
        # Load pickle data
        pickle_data = load_pickle_data(args.pickle_file)
        print()
        
        # Validate pickle data
        if not validate_pickle_data(pickle_data):
            raise Exception("Invalid pickle data structure")
        print()
        
        # Create SQLite database
        conn = create_sqlite_database(args.sqlite_file)
        print()
        
        # Migrate tasks
        tasks_migrated = migrate_tasks(conn, pickle_data['tasks'])
        print()
        
        # Migrate kanban
        kanban_migrated = migrate_kanban(conn, pickle_data['kanban'])
        print()
        
        # Verify migration
        if not args.no_verify:
            if not verify_migration(conn, pickle_data):
                raise Exception("Migration verification failed")
            print()
        
        # Close connection
        conn.close()
        
        # Success message
        print("=" * 60)
        print("✓ MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Pickle file: {args.pickle_file}")
        print(f"SQLite database: {args.sqlite_file}")
        print(f"Tasks migrated: {tasks_migrated}")
        print(f"Kanban columns migrated: {kanban_migrated}")
        
        if args.backup:
            print(f"\nBackup created at: {backup_path}")
        
        print("\nYou can now use the new SQLite-based DataStorage class.")
        print("The old pickle file is still available if you need to roll back.")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ MIGRATION FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nNo changes were made to your data.")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())