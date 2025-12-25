@echo off
echo ============================================================
echo COMPLETE FIX FOR DATA FILES NOT LOADING IN CLOUD RUN
echo ============================================================
echo.

echo STEP 1: Add data files to git (if not already tracked)
echo ------------------------------------------------------------
git add data/*.csv
git add data/*.json
git add data/*.npy
git add api/data/*.csv
git add api/data/*.json  
git add api/data/*.npy
echo Done.
echo.

echo STEP 2: Commit the data files
echo ------------------------------------------------------------
git commit -m "Add data files for production deployment"
echo.

echo STEP 3: Verify files are staged
echo ------------------------------------------------------------
echo Data files in git:
git ls-files data/*.csv api/data/*.csv
echo.

echo STEP 4: Check .dockerignore
echo ------------------------------------------------------------
type .dockerignore | findstr /C:"csv"
echo.
echo NOTE: Make sure lines with *.csv and data/*.csv are COMMENTED OUT (have # in front)
echo.

echo STEP 5: Ready to deploy
echo ------------------------------------------------------------
echo Run this command to deploy:
echo    gcloud builds submit --config cloudbuild.yaml
echo.
echo Or if using docker directly:
echo    gcloud run deploy brandfluence --source . --region us-central1
echo.
echo ============================================================
echo IMPORTANT: After deployment, check the build logs!
echo.
echo Look for the "VERIFYING DATA FILES" section in the build output.
echo It should show: "✓ influenceurs_recommendation_ready.csv found"
echo ============================================================
pause
