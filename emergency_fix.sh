#!/bin/bash
# EMERGENCY FIX - Add CSV files to git and deploy

echo "=========================================="
echo "EMERGENCY FIX - Adding CSV files to git"
echo "=========================================="
echo ""

# Step 1: Check what CSV files we have locally
echo "Step 1: CSV files that exist locally:"
find data/ api/data/ -name "*.csv" -type f 2>/dev/null
echo ""

# Step 2: Check what's currently tracked
echo "Step 2: CSV files currently tracked by git:"
git ls-files data/*.csv api/data/*.csv 2>/dev/null || echo "  NONE - This is the problem!"
echo ""

# Step 3: Add all CSV files
echo "Step 3: Adding CSV files to git..."
git add -f data/*.csv
git add -f api/data/*.csv
git add -f data/*.json
git add -f data/*.npy
git add -f api/data/*.npy
echo "Done"
echo ""

# Step 4: Verify what will be committed
echo "Step 4: Files staged for commit:"
git diff --cached --name-only | grep -E "\\.csv$|\\.json$|\\.npy$" || echo "  WARNING: No files staged!"
echo ""

# Step 5: Show file sizes
echo "Step 5: File sizes:"
git diff --cached --stat | grep -E "\\.csv|\\.json|\\.npy"
echo ""

# Step 6: Commit
echo "Step 6: Committing files..."
git commit -m "Add data files (CSV, JSON, NPY) for production deployment

- Required for recommender system in Cloud Run
- Files were excluded from previous builds
- Total CSV files needed for API to function"
echo ""

# Step 7: Verify files are now tracked
echo "Step 7: Verification - Files now in git:"
git ls-files data/*.csv data/*.json data/*.npy api/data/*.csv api/data/*.npy
echo ""

echo "=========================================="
echo "SUCCESS! Now deploy with:"
echo "  gcloud builds submit --config cloudbuild.yaml"
echo ""
echo "Or:"
echo "  git push  # if using git-based deployment"
echo "=========================================="
