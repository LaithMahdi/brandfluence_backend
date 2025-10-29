# Vercel Cleanup Guide

After successfully deploying to Render, follow these steps to clean up Vercel-related files and configurations.

## Files to Delete

Run these commands to remove Vercel-specific files:

```bash
# Delete Vercel configuration files
del vercel.json
del vercel_app.py

# Delete Vercel documentation files
del VERCEL_DEPLOYMENT.md
del VERCEL_FIX.md
del VERCEL_TROUBLESHOOTING.md

# Delete old deployment files if not needed
del DEPLOY_QUICK.md
del DEPLOYMENT_CHECKLIST.md
del DEPLOYMENT_SUMMARY.md
```

Or manually delete these files from your project:

- `vercel.json`
- `vercel_app.py`
- `VERCEL_DEPLOYMENT.md`
- `VERCEL_FIX.md`
- `VERCEL_TROUBLESHOOTING.md`
- `DEPLOY_QUICK.md` (if Vercel-specific)
- `DEPLOYMENT_CHECKLIST.md` (if Vercel-specific)
- `DEPLOYMENT_SUMMARY.md` (if Vercel-specific)

## Update .gitignore

Add these lines to your `.gitignore` if not already present:

```
# Render
.render/

# Static files
staticfiles/
staticfiles_build/
```

## Vercel Dashboard Cleanup

1. Go to https://vercel.com/dashboard
2. Find your `brandfluence-backend` project
3. Click on the project
4. Go to Settings
5. Scroll to bottom and click "Delete Project"
6. Confirm deletion

## Environment Variables

Your `.env` file has been kept intact and works with Render. No changes needed.

## Git Commit

After cleaning up, commit your changes:

```bash
git add .
git commit -m "Remove Vercel config and migrate to Render"
git push origin main
```

This will trigger an automatic deployment on Render if you've configured auto-deploy.

## Verify Migration

1. Check that your Render deployment is working: `https://your-app.onrender.com/graphql/`
2. Test all GraphQL queries and mutations
3. Verify email functionality
4. Test authentication flows
5. Update frontend to use new Render URL

## Rollback Plan (Just in Case)

If you need to rollback to Vercel:

1. The old files are in your git history
2. Run: `git revert HEAD` to undo the cleanup commit
3. Redeploy to Vercel

## Optional: Remove Old Build Files

```bash
# Remove old build directories
rmdir /s /q staticfiles_build
```

---

**Note**: Only perform this cleanup after confirming your Render deployment is fully functional and tested.
