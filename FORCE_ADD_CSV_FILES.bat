@echo off
SETLOCAL EnableDelayedExpansion

echo ============================================================
echo FINAL FIX - Force Add CSV Files to Git
echo ============================================================
echo.

cd /d "%~dp0"

echo [1] Current directory:
cd
echo.

echo [2] Checking what CSV files exist locally:
echo ------------------------------------------------------------
for %%f in (data\*.csv) do (
    echo    FOUND: %%f
    set "found_csv=1"
)
for %%f in (api\data\*.csv) do (
    echo    FOUND: %%f
    set "found_csv=1"
)
if not defined found_csv (
    echo    ERROR: No CSV files found locally!
    echo    You need CSV files to deploy. Check your data directory.
    pause
    exit /b 1
)
echo.

echo [3] Checking what git currently tracks:
echo ------------------------------------------------------------
git ls-files data/ api/data/ | findstr /i "\.csv"
if errorlevel 1 (
    echo    WARNING: No CSV files tracked by git - this is the problem!
) else (
    echo    Some CSV files are tracked
)
echo.

echo [4] Force adding ALL CSV files to git:
echo ------------------------------------------------------------
git add -f data\influenceurs_recommendation_ready.csv
git add -f data\influenceurs_clean.csv
git add -f data\Top_Influencers_Full_1500.csv
git add -f api\data\influenceurs_recommendation_ready.csv
git add -f data\*.json
git add -f data\*.npy
git add -f api\data\*.npy
echo Done
echo.

echo [5] Checking what's now staged for commit:
echo ------------------------------------------------------------
git diff --cached --name-only
echo.

echo [6] Showing file sizes that will be committed:
echo ------------------------------------------------------------
git diff --cached --stat
echo.

echo [7] Committing files:
echo ------------------------------------------------------------
git commit -m "PRODUCTION FIX: Add CSV data files required for recommender API

- influenceurs_recommendation_ready.csv
- influenceurs_clean.csv  
- Top_Influencers_Full_1500.csv
- Required for /api/recommend/ endpoint to work
- Without these files, API returns 503 errors"

if errorlevel 1 (
    echo.
    echo WARNING: Commit failed or no changes to commit
    echo Checking if files are already committed...
    git log --oneline -n 5 | findstr /i "csv data"
    echo.
)
echo.

echo [8] Verification - Files now tracked by git:
echo ------------------------------------------------------------
git ls-files data/*.csv api/data/*.csv
echo.

echo ============================================================
echo SUCCESS! Now deploy:
echo.
echo    gcloud builds submit --config cloudbuild.yaml
echo.
echo After deployment, check the build logs for:
echo    "Files in data/: [...CSV files should be listed here...]"
echo ============================================================
echo.
pause
