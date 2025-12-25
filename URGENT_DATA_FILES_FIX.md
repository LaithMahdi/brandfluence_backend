# URGENT FIX - Data Files Not Loading

## The Problem

Your `.dockerignore` file was **excluding all CSV and data files** from the Docker image. This is why you're getting:

```json
{
  "error": "Recommender data not available. Please contact administrator.",
  "debug_info": "Data file was not loaded during initialization"
}
```

## What Was Fixed

### 1. `.dockerignore` - COMMENTED OUT data file exclusions

```ignore
# Data files - KEEP THESE FOR PRODUCTION!
# *.csv              ← COMMENTED OUT
# *.json             ← COMMENTED OUT
# data/*.csv         ← COMMENTED OUT
# data/*.json        ← COMMENTED OUT
# data/*.npy         ← COMMENTED OUT
```

### 2. `Dockerfile` - Added comprehensive verification

- Runs `verify_data_files.py` during build
- Lists all directories and CSV files
- Shows detailed output in build logs

### 3. `verify_data_files.py` - NEW diagnostic script

- Checks all possible data locations
- Verifies file sizes and pandas loading
- Can be run locally or in production

## Deploy NOW

```bash
# 1. Verify files exist locally FIRST
python verify_data_files.py

# 2. If files exist locally, rebuild and deploy
gcloud builds submit --config cloudbuild.yaml

# 3. Watch the build logs for data file verification
# You should see output from verify_data_files.py showing files were found

# 4. After deployment, check runtime logs
gcloud run logs read brandfluence --region us-central1 --limit 100 | grep -i "data\|csv\|influenc"

# 5. Test the API
curl "https://brandfluence-251801873872.us-central1.run.app/api/recommend/?category=Fashion&country=USA&n=5"
```

## Expected Build Output

During `gcloud builds submit`, you should now see:

```
========================================
VERIFYING DATA FILES...
========================================
📁 Base Directory: /app
📁 Current Working Dir: /app

🔍 Checking data directories:
  ✓ /app/data - EXISTS
  ✓ /app/api/data - EXISTS

🔍 Searching for CSV files:
  In /app/data:
    ✓ influenceurs_recommendation_ready.csv (2.34 MB)
    ✓ influenceurs_clean.csv (1.89 MB)

✓ STATUS: Data files are available!
========================================
```

## If Files Are Still Missing

### Check 1: Are files committed to git?

```bash
cd c:\Users\SBS\Music\brandfluence
git status data/
ls data/*.csv
```

If files are not tracked by git:

```bash
git add data/*.csv
git add data/*.json
git add data/*.npy
git commit -m "Include data files for production"
git push
```

### Check 2: Verify .gitignore doesn't exclude them

Edit `.gitignore` and make sure these lines are commented out or removed:

```ignore
# data/*.csv    ← Should be commented out
# *.csv         ← Should be commented out
```

### Check 3: Build locally to test

```bash
docker build -t brandfluence-test .
docker run --rm brandfluence-test python verify_data_files.py
```

## Why This Happened

The `.dockerignore` file had these lines:

```ignore
*.csv
data/*.csv
data/*.json
data/*.npy
```

This told Docker to **exclude all CSV files** when building the image, so even though the files were in your local repo, they weren't being copied to the container.

## After Deployment

Once deployed successfully, your logs should show:

```
INFO Initializing recommender. BASE_DIR: /app
INFO Checking 8 possible data file locations...
INFO 1. /app/data/influenceurs_recommendation_ready.csv - FOUND
✓ Using data file: /app/data/influenceurs_recommendation_ready.csv
✓ Données chargées: 1500 influenceurs
✓ Categories: 15, Countries: 25
```

And your API will work:

```bash
curl "https://brandfluence-251801873872.us-central1.run.app/api/recommend/?category=Fashion&country=USA&n=5"
# Should return recommendations instead of error
```
