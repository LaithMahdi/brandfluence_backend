"""
Automated Token Cleanup Scheduler
This script runs the cleanup_expired_tokens command automatically at scheduled intervals.

Usage:
    Activate virtual environment first, then run:
    python run_token_cleanup.py

Default: Runs cleanup every day at 2:00 AM
You can modify the schedule in the code below.
"""

import schedule
import time
import subprocess
import os
import sys
from datetime import datetime


def run_cleanup():
    """Execute the token cleanup command"""
    try:
        print(f"\n[{datetime.now()}] Starting token cleanup...")
        
        # Get the Python executable from current environment
        python_executable = sys.executable
        
        # Run the Django management command using the same Python interpreter
        result = subprocess.run(
            [python_executable, 'manage.py', 'cleanup_expired_tokens'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] ✓ Token cleanup completed successfully")
        else:
            print(f"[{datetime.now()}] ✗ Token cleanup failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
                
    except Exception as e:
        print(f"[{datetime.now()}] ✗ Error running cleanup: {e}")


def main():
    print("=" * 60)
    print("Token Cleanup Scheduler Started")
    print("=" * 60)
    print(f"Python: {sys.executable}")
    print("Schedule: Daily at 2:00 AM")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Schedule the cleanup
    # Run every day at 2:00 AM
    schedule.every().day.at("02:00").do(run_cleanup)
    
    # Alternative schedules (uncomment to use):
    # schedule.every().hour.do(run_cleanup)  # Run every hour
    # schedule.every(6).hours.do(run_cleanup)  # Run every 6 hours
    # schedule.every().day.at("00:00").do(run_cleanup)  # Run at midnight
    
    # Run once immediately on startup
    print(f"\n[{datetime.now()}] Running initial cleanup...")
    run_cleanup()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
