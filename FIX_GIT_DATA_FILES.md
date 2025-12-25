# CRITICAL FIX - Data Files Must Be Committed to Git

## The Real Problem

Your CSV files exist locally but are **NOT committed to git**. When Google Cloud Build runs, it clones your git repository - if the files aren't in git, they won't be in the build!

## Quick Fix - Run These Commands

### Option 1: Run the automated script

```bash
.\fix_and_deploy.bat
```

### Option 2: Manual steps

```bash
# 1. Add data files to git
git add data/*.csv data/*.json data/*.npy
git add api/data/*.csv api/data/*.npy

# 2. Commit them
git commit -m "Add data files for production deployment"

# 3. Push to your repository
git push

# 4. Deploy
gcloud builds submit --config cloudbuild.yaml
```

## Verify Before Deploying

Check if files are tracked:

```bash
git ls-files data/*.csv api/data/*.csv
```

**You should see:**

```
data/influenceurs_clean.csv
data/influenceurs_recommendation_ready.csv
data/Top_Influencers_Full_1500.csv
api/data/influenceurs_recommendation_ready.csv
```

**If you see nothing**, the files aren't tracked and won't be deployed!

## Why This Happened

1. ✅ Files exist locally (we confirmed this)
2. ✅ .gitignore doesn't exclude them (no `*.csv` pattern)
3. ✅ .dockerignore is fixed (patterns are commented out)
4. ❌ **But files were never added to git** (this is the issue!)

When you run `gcloud builds submit`, it:

1. Creates a tarball from your git repository
2. Uploads it to Google Cloud Build
3. **Only includes files tracked by git**

If files aren't in git → they aren't in the build → they aren't in the container → you get "data not available"

## After Fixing

Once you've committed and deployed, verify it worked:

### 1. Check build logs

```bash
gcloud builds list --limit 1
# Get the ID of the latest build
gcloud builds log <BUILD_ID>
```

Look for this in the output:

```
========================================
VERIFYING DATA FILES...
========================================
✓ influenceurs_recommendation_ready.csv found at /app/data/influenceurs_recommendation_ready.csv (2.34 MB)
✓ STATUS: Data files are available!
```

### 2. Check runtime logs

```bash
gcloud run logs read brandfluence --region us-central1 --limit 50
```

You should see:

```
INFO Initializing recommender. BASE_DIR: /app
INFO Using data file: /app/data/influenceurs_recommendation_ready.csv
✓ Données chargées: 1500 influenceurs
```

### 3. Test the API

```bash
curl "https://brandfluence-251801873872.us-central1.run.app/api/recommend/?category=Fashion&country=USA&n=5"
```

Should return recommendations, not an error!

## Still Having Issues?

### Check 1: Are you using Google Cloud Build or Cloud Run Source Deploy?

If using **cloudbuild.yaml**:

- Files MUST be in git
- Run: `git ls-files` to see what's tracked

If using **gcloud run deploy --source**:

- Files must be in local directory
- But still respects .dockerignore

### Check 2: Which files do you actually have?

```bash
# See what's in your workspace
ls -la data/
ls -la api/data/

# See what's tracked by git
git ls-files data/ api/data/
```

### Check 3: Size limits

CSV files can be large. If they're over 100MB:

- Consider using Git LFS
- Or host them externally and download during startup
- Or bake them into a custom base image

## Alternative: Use Cloud Storage

If files are too large or you don't want them in git:

1. Upload to Google Cloud Storage:

```bash
gsutil mb gs://brandfluence-data
gsutil cp data/*.csv gs://brandfluence-data/
```

2. Modify your app to download on startup:

```python
from google.cloud import storage

def download_data_files():
    client = storage.Client()
    bucket = client.bucket('brandfluence-data')

    blob = bucket.blob('influenceurs_recommendation_ready.csv')
    blob.download_to_filename('/app/data/influenceurs_recommendation_ready.csv')
```

3. Add to requirements.txt:

```
google-cloud-storage
```

But for now, the simplest fix is: **Commit the files to git!**
