# Token Cleanup Scripts

This directory contains scripts to automatically delete expired verification tokens and password reset tokens from the database.

## Files

1. **`cleanup_expired_tokens.py`** - Django management command (in `users/management/commands/`)
2. **`cleanup_tokens.bat`** - Windows batch script for manual/scheduled execution
3. **`run_token_cleanup.py`** - Python scheduler for automatic execution

---

## Option 1: Manual Cleanup

Run the cleanup command manually whenever you need:

```bash
python manage.py cleanup_expired_tokens
```

### Command Options

- **Dry run** (preview what will be deleted):

  ```bash
  python manage.py cleanup_expired_tokens --dry-run
  ```

- **Delete tokens older than X days** (in addition to expired ones):

  ```bash
  python manage.py cleanup_expired_tokens --days 30
  ```

- **Combine options**:
  ```bash
  python manage.py cleanup_expired_tokens --days 30 --dry-run
  ```

---

## Option 2: Automated Cleanup (Python Scheduler)

Use the Python scheduler to run cleanup automatically.

### Installation

First, install the required package:

```bash
pip install schedule
```

### Run the Scheduler

```bash
python run_token_cleanup.py
```

This will:

- Run cleanup immediately on startup
- Run cleanup every day at 2:00 AM
- Keep running in the background

### Customize Schedule

Edit `run_token_cleanup.py` and modify the schedule line:

```python
# Daily at 2:00 AM (default)
schedule.every().day.at("02:00").do(run_cleanup)

# Every hour
schedule.every().hour.do(run_cleanup)

# Every 6 hours
schedule.every(6).hours.do(run_cleanup)

# At midnight
schedule.every().day.at("00:00").do(run_cleanup)
```

### Run as Background Service

**Windows (using pythonw):**

```bash
start /B pythonw run_token_cleanup.py
```

**Windows (using Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup" or "Daily")
4. Action: Start a program
5. Program: `pythonw.exe`
6. Arguments: `run_token_cleanup.py`
7. Start in: `D:\brandfluence_backend`

---

## Option 3: Windows Task Scheduler (Batch File)

Use Windows Task Scheduler to run the batch file automatically.

### Setup Steps

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. Name: "Cleanup Expired Tokens"
4. Trigger: **Daily** at your preferred time (e.g., 2:00 AM)
5. Action: **Start a program**
6. Program/script: Browse to `cleanup_tokens.bat`
7. Start in: `D:\brandfluence_backend`
8. Click **Finish**

---

## Option 4: Linux Cron Job (Production)

For Linux servers, use cron:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2:00 AM)
0 2 * * * cd /path/to/brandfluence_backend && /path/to/venv/bin/python manage.py cleanup_expired_tokens >> /path/to/logs/token_cleanup.log 2>&1
```

---

## What Gets Deleted?

The script deletes:

- ✓ Verification tokens that have passed their `expires_at` date
- ✓ Password reset tokens that have passed their `expires_at` date
- ✓ Optionally: Tokens older than X days (using `--days` parameter)

The script preserves:

- ✗ Valid (non-expired) tokens
- ✗ Tokens still within their validity period

---

## Monitoring

### Check Token Statistics

```bash
python manage.py shell
```

```python
from users.models import VerifyToken, PasswordResetToken
from django.utils import timezone

# Count total tokens
print(f"Verify tokens: {VerifyToken.objects.count()}")
print(f"Reset tokens: {PasswordResetToken.objects.count()}")

# Count expired tokens
now = timezone.now()
expired_verify = VerifyToken.objects.filter(expires_at__lt=now).count()
expired_reset = PasswordResetToken.objects.filter(expires_at__lt=now).count()
print(f"Expired verify tokens: {expired_verify}")
print(f"Expired reset tokens: {expired_reset}")
```

---

## Best Practices

1. **Run daily** - Schedule cleanup to run at least once per day during low-traffic hours (2-4 AM)
2. **Test first** - Always use `--dry-run` to preview deletions before running in production
3. **Monitor logs** - Check execution logs regularly to ensure cleanup is working
4. **Set retention** - Use `--days 30` to also delete old tokens (recommended: 30-90 days)
5. **Database backups** - Ensure regular backups before automated deletion

---

## Troubleshooting

**Issue: "No module named 'schedule'"**

```bash
pip install schedule
```

**Issue: Permission denied**

- Ensure virtual environment is activated
- Check file permissions on Windows

**Issue: Task doesn't run automatically**

- Verify Task Scheduler task is enabled
- Check task history in Task Scheduler
- Ensure correct Python path and working directory

---

## Production Deployment

For production servers (Render, Heroku, etc.), add to your deployment:

**Render** - Add a Cron Job:

```yaml
# render.yaml
services:
  - type: cron
    name: cleanup-tokens
    env: python
    schedule: "0 2 * * *" # Daily at 2 AM
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python manage.py cleanup_expired_tokens"
```

**Heroku** - Use Heroku Scheduler:

```bash
# Add Heroku Scheduler addon
heroku addons:create scheduler:standard

# Then in Heroku Dashboard > Scheduler, add:
python manage.py cleanup_expired_tokens
```

---

## Summary

- **Manual**: `python manage.py cleanup_expired_tokens`
- **Automated (Python)**: `python run_token_cleanup.py`
- **Automated (Windows)**: Use Task Scheduler with `cleanup_tokens.bat`
- **Automated (Linux)**: Use cron job
