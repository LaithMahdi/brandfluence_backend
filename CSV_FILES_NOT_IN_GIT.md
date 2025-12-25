# Critical Diagnostic - CSV Files Not Deploying

## Current Status

✅ `.npy` files ARE in container: `feature_matrix.npy` is present  
❌ `.csv` files are NOT in container: all CSV files missing

This proves:

- Docker build is working
- File copying is working
- But CSV files specifically are not being included

## Root Cause

**CSV files are not committed to git**

Even though:

- ✅ Files exist locally
- ✅ `.gitignore` doesn't exclude them
- ✅ `.dockerignore` has CSV patterns commented out

The files were never added to git in the first place!

## How to Verify

### Check what's in your git repo:

```bash
git ls-files data/ api/data/
```

**If you DON'T see CSV files listed**, they're not in git and won't deploy.

### Check what's staged:

```bash
git status data/ api/data/
```

If CSV files show as "Untracked", they need to be added.

## The Fix - 3 Commands

```bash
# 1. Force add CSV files (ignoring any exclude patterns)
git add -f data/influenceurs_recommendation_ready.csv
git add -f data/influenceurs_clean.csv
git add -f data/Top_Influencers_Full_1500.csv
git add -f api/data/influenceurs_recommendation_ready.csv

# 2. Commit
git commit -m "Add CSV data files for production deployment"

# 3. Verify
git ls-files data/ | grep csv
```

**You MUST see CSV files listed after step 3!**

## Then Deploy

```bash
gcloud builds submit --config cloudbuild.yaml
```

Watch the build output. You should see different results in the verification step showing CSV files are now present.

## Why `git add -f`?

The `-f` (force) flag ensures files are added even if:

- There are exclude patterns somewhere
- Files were previously ignored
- Git is configured to ignore certain patterns

## After Deployment

The logs should show:

```
Files in data/: ['feature_matrix.npy', 'influenceurs_recommendation_ready.csv', 'influenceurs_clean.csv', ...]
```

Instead of just:

```
Files in data/: ['feature_matrix.npy']
```

## Alternative: Use Git LFS

If CSV files are very large (>100MB), you might need Git LFS:

```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes
git add data/*.csv
git commit -m "Add CSV files with LFS"
```

## Run the Automated Fix

```bash
.\FORCE_ADD_CSV_FILES.bat
```

This script will:

1. ✅ Check files exist locally
2. ✅ Force add all CSV files
3. ✅ Show what's being committed
4. ✅ Commit with descriptive message
5. ✅ Verify files are tracked
