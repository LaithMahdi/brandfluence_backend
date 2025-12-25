#!/usr/bin/env python3
"""
Verify that data files are present and accessible
Run this script both locally and in production to diagnose data loading issues
"""
import os
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("DATA FILES VERIFICATION")
    print("=" * 60)
    
    # Get base directory
    base_dir = Path(__file__).resolve().parent
    print(f"\n📁 Base Directory: {base_dir}")
    print(f"📁 Current Working Dir: {os.getcwd()}")
    
    # Check data directories
    data_dirs = [
        base_dir / 'data',
        base_dir / 'api' / 'data',
        Path('/app/data'),
        Path('/app/api/data'),
    ]
    
    print(f"\n🔍 Checking data directories:")
    found_dirs = []
    for data_dir in data_dirs:
        exists = data_dir.exists()
        print(f"  {'✓' if exists else '✗'} {data_dir} - {'EXISTS' if exists else 'not found'}")
        if exists:
            found_dirs.append(data_dir)
    
    # Check for CSV files
    print(f"\n🔍 Searching for CSV files:")
    csv_files = []
    
    for data_dir in found_dirs:
        csv_in_dir = list(data_dir.glob('*.csv'))
        if csv_in_dir:
            print(f"\n  In {data_dir}:")
            for csv_file in csv_in_dir:
                size_mb = csv_file.stat().st_size / (1024 * 1024)
                print(f"    ✓ {csv_file.name} ({size_mb:.2f} MB)")
                csv_files.append(csv_file)
        else:
            print(f"  ✗ No CSV files in {data_dir}")
    
    # Check for specific required files
    print(f"\n🔍 Checking for required files:")
    required_files = [
        'influenceurs_recommendation_ready.csv',
        'influenceurs_clean.csv',
    ]
    
    found_required = False
    for req_file in required_files:
        found = False
        for data_dir in found_dirs:
            file_path = data_dir / req_file
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                print(f"  ✓ {req_file} found at {file_path} ({size_mb:.2f} MB)")
                found = True
                found_required = True
                break
        if not found:
            print(f"  ✗ {req_file} NOT FOUND")
    
    # Try loading with pandas
    print(f"\n🔍 Testing pandas loading:")
    try:
        import pandas as pd
        if csv_files:
            test_file = csv_files[0]
            df = pd.read_csv(test_file)
            print(f"  ✓ Successfully loaded {test_file.name}")
            print(f"  ✓ Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"  ✓ Columns: {list(df.columns)}")
        else:
            print(f"  ✗ No CSV files to test")
    except ImportError:
        print(f"  ⚠ pandas not installed")
    except Exception as e:
        print(f"  ✗ Error loading CSV: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY:")
    print(f"  Data directories found: {len(found_dirs)}")
    print(f"  CSV files found: {len(csv_files)}")
    print(f"  Required files found: {'YES' if found_required else 'NO'}")
    
    if found_required:
        print(f"\n✓ STATUS: Data files are available!")
        return 0
    else:
        print(f"\n✗ STATUS: Required data files are MISSING!")
        print(f"\n💡 TROUBLESHOOTING:")
        print(f"  1. Check .dockerignore - ensure CSV files are not excluded")
        print(f"  2. Check .gitignore - ensure data files are committed to git")
        print(f"  3. Verify files exist locally: ls -la data/*.csv")
        print(f"  4. After fixing, rebuild: gcloud builds submit")
        return 1

if __name__ == '__main__':
    sys.exit(main())
