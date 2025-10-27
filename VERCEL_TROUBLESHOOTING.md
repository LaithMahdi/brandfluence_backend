# Vercel 500 Error - Troubleshooting Guide

## 🔍 Error: FUNCTION_INVOCATION_FAILED

This error means the Django application crashed when Vercel tried to run it.

## ✅ Fixes Applied

### 1. Updated `vercel.json`

- Changed from `brandfluence/wsgi.py` to `vercel_app.py`
- Simplified routing

### 2. Updated `vercel_app.py`

- Added proper path configuration
- Ensured Django settings module is set correctly

### 3. Updated Settings

- Added automatic Vercel URL detection for `ALLOWED_HOSTS`
- Added `CSRF_TRUSTED_ORIGINS` for Vercel
- Improved database configuration with health checks

### 4. Added Health Check Endpoint

- Root URL (`/`) now returns a JSON health check
- Helps verify the app is running

## 🚨 Most Likely Cause: Missing DATABASE_URL

The #1 reason for this error is **missing or invalid DATABASE_URL**.

### Required: Set DATABASE_URL in Vercel

Go to Vercel Dashboard → Your Project → Settings → Environment Variables

Add:

```
DATABASE_URL=postgresql://user:password@host:port/database
```

**⚠️ IMPORTANT**:

- SQLite does NOT work on Vercel (read-only filesystem)
- You MUST use PostgreSQL

## 📊 Get Free PostgreSQL Database

### Option 1: Neon (Recommended)

1. Go to https://neon.tech
2. Sign up (free)
3. Create new project
4. Copy connection string
5. Add to Vercel as `DATABASE_URL`

### Option 2: Supabase

1. Go to https://supabase.com
2. Create project
3. Settings → Database → Connection string
4. Use "Connection pooling" URI
5. Add to Vercel as `DATABASE_URL`

### Option 3: Railway

1. Go to https://railway.app
2. Create PostgreSQL database
3. Copy connection string
4. Add to Vercel as `DATABASE_URL`

## 🔧 After Adding DATABASE_URL

### 1. Redeploy

- Go to Vercel Dashboard
- Click "Redeploy"

### 2. Run Migrations

You need to run migrations on your production database:

```bash
# Method 1: From local machine
export DATABASE_URL="your-production-database-url"
python manage.py migrate
python manage.py createsuperuser
```

```powershell
# Method 1: Windows PowerShell
$env:DATABASE_URL="your-production-database-url"
python manage.py migrate
python manage.py createsuperuser
```

## 🧪 Test Your Deployment

### 1. Health Check

Visit: `https://your-project.vercel.app/`

Should return:

```json
{
  "status": "ok",
  "django_version": "5.2.7",
  "message": "BrandFluence API is running"
}
```

### 2. GraphQL Endpoint

Visit: `https://your-project.vercel.app/graphql/`

Should show GraphQL Playground

### 3. Test Query

```graphql
query {
  __schema {
    queryType {
      name
    }
  }
}
```

## 📋 Complete Environment Variables Checklist

Make sure ALL these are set in Vercel:

### Required ✅

- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `SECRET_KEY` - Generated secret key (run `python generate_secret_key.py`)

### Recommended 👍

- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - `.vercel.app` (or auto-detected)

### Optional

- [ ] `CORS_ALLOW_ALL_ORIGINS` - `False` (more secure)
- [ ] `CORS_ALLOWED_ORIGINS` - Your frontend URLs

## 🐛 Still Getting 500 Error?

### Check Vercel Function Logs

1. Go to Vercel Dashboard
2. Click on your deployment
3. Click "Functions" tab
4. Look for error messages in logs

Common error messages:

#### "No module named 'psycopg2'"

Already in requirements.txt, should not happen. If it does, add:

```
psycopg2-binary==2.9.10
```

#### "relation does not exist"

Database tables not created. Run migrations:

```bash
python manage.py migrate
```

#### "DisallowedHost"

Fixed automatically now, but if persists, set `ALLOWED_HOSTS`:

```
ALLOWED_HOSTS=.vercel.app,your-custom-domain.com
```

#### "CSRF verification failed"

Visit via HTTPS (not HTTP). Fixed with `CSRF_TRUSTED_ORIGINS`.

## 🔄 Deployment Steps Summary

1. **Set DATABASE_URL** in Vercel environment variables
2. **Generate SECRET_KEY**: `python generate_secret_key.py`
3. **Add SECRET_KEY** to Vercel
4. **Commit and push** changes
5. **Redeploy** in Vercel
6. **Run migrations** with production DATABASE_URL
7. **Create superuser**
8. **Test** health check endpoint

## ✨ Expected Working URLs

After successful deployment:

- 🏠 Health Check: `https://your-project.vercel.app/`
- 🔍 GraphQL API: `https://your-project.vercel.app/graphql/`
- 👨‍💼 Admin Panel: `https://your-project.vercel.app/admin/`
- 📊 Schema Viewer: `https://your-project.vercel.app/schema/`

## 📞 Need More Help?

Check these files:

- `VERCEL_DEPLOYMENT.md` - Full deployment guide
- `DEPLOY_QUICK.md` - Quick start guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist

Common issues are almost always:

1. Missing `DATABASE_URL` ⭐ **Most common**
2. Invalid PostgreSQL connection string
3. Database tables not migrated
4. Missing `SECRET_KEY`

Fix these and your app will work! 🚀
