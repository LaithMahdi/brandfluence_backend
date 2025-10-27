# Vercel Deployment - Files Created/Modified

## ✅ Files Created

1. **`vercel.json`** - Vercel deployment configuration
2. **`build_files.sh`** - Build script for collecting static files
3. **`vercel_app.py`** - WSGI application entry point for Vercel
4. **`.vercelignore`** - Files to exclude from deployment
5. **`VERCEL_DEPLOYMENT.md`** - Complete deployment guide
6. **`DEPLOY_QUICK.md`** - Quick start guide
7. **`static/.gitkeep`** - Static files directory

## 🔧 Files Modified

1. **`brandfluence/settings.py`**

   - Added `ALLOWED_HOSTS = ['*']` (configure in env vars for production)
   - Added static files configuration (STATIC_ROOT, STATICFILES_DIRS)
   - Added media files configuration
   - Added WhiteNoise middleware for static file serving
   - Updated CORS settings to be configurable via environment variables
   - Added WhiteNoise storage backend

2. **`requirements.txt`**
   - Added `whitenoise==6.6.0` for serving static files

## 🚀 Deployment Steps

### Quick Deploy (5 minutes)

1. **Push to Git**

   ```bash
   git add .
   git commit -m "Configure for Vercel"
   git push
   ```

2. **Import to Vercel**

   - Go to https://vercel.com/new
   - Import your repository
   - Deploy

3. **Add Environment Variables** in Vercel dashboard:

   ```
   SECRET_KEY=generate-a-new-secret-key
   DEBUG=False
   ALLOWED_HOSTS=.vercel.app
   DATABASE_URL=postgresql://user:pass@host:port/db
   CORS_ALLOW_ALL_ORIGINS=False
   CORS_ALLOWED_ORIGINS=https://your-frontend.com
   ```

4. **Redeploy** after adding environment variables

### Database Setup

You need PostgreSQL for production. Choose one:

- **Neon**: https://neon.tech (Free tier available)
- **Supabase**: https://supabase.com (Free tier available)
- **Railway**: https://railway.app (Free trial)

Get the `DATABASE_URL` and add it to Vercel environment variables.

### After First Deployment

1. Run migrations on production DB (locally):

   ```bash
   export DATABASE_URL=your-production-db-url
   python manage.py migrate
   ```

2. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

## 📝 Environment Variables Reference

### Required

- `SECRET_KEY` - Django secret key (generate new one for production)
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### Optional

- `DEBUG` - Set to `False` in production
- `CORS_ALLOW_ALL_ORIGINS` - Set to `False` in production
- `CORS_ALLOWED_ORIGINS` - Comma-separated frontend URLs

## 🎯 Your API Endpoints

After deployment:

- GraphQL API: `https://your-project.vercel.app/graphql/`
- Admin Panel: `https://your-project.vercel.app/admin/`

## ⚠️ Important Notes

1. **Database**: Must use PostgreSQL (not SQLite) on Vercel
2. **Static Files**: Automatically handled by WhiteNoise
3. **Media Files**: For file uploads, use cloud storage (S3, Cloudinary)
4. **Serverless Limits**: 10s timeout (Hobby), 60s (Pro)
5. **Security**: Never commit `.env` file with real credentials

## 📚 Documentation

- Quick Start: `DEPLOY_QUICK.md`
- Full Guide: `VERCEL_DEPLOYMENT.md`
- Authentication: `users/AUTHENTICATION.md`
- Auth Examples: `users/AUTH_EXAMPLES.md`

## ✅ Verification Checklist

Before deploying to production:

- [ ] Generated new `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configured PostgreSQL database
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Configured CORS properly
- [ ] Tested authentication flow
- [ ] Created superuser
- [ ] Tested GraphQL endpoints
- [ ] Reviewed security settings

## 🔗 Next Steps

1. Deploy to Vercel
2. Set up database
3. Run migrations
4. Create superuser
5. Test API endpoints
6. Configure custom domain (optional)
7. Set up monitoring (optional)

## 💡 Tips

- Use Vercel's preview deployments for testing
- Monitor logs in Vercel dashboard
- Enable branch deployments for staging
- Set up GitHub Actions for tests (optional)

## 🆘 Need Help?

- Check `VERCEL_DEPLOYMENT.md` for troubleshooting
- Vercel Docs: https://vercel.com/docs
- Django on Vercel: https://vercel.com/guides/deploying-django-with-vercel
