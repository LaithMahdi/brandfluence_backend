# Quick Reference: Render Deployment Steps

## 1. Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## 2. Create Web Service on Render

- Go to: https://dashboard.render.com/
- Click "New +" → "Web Service"
- Connect GitHub repo: `LaithMahdi/brandfluence_backend`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn brandfluence.wsgi:application`

## 3. Set Environment Variables

Copy-paste these in Render dashboard:

```
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
DATABASE_URL=postgresql://neondb_owner:npg_l9Y2wObTsSqF@ep-still-mouse-ahqqpbr8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
ALLOWED_HOSTS=<your-render-url>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-render-url>.onrender.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=brandfluence@gmail.com
EMAIL_HOST_PASSWORD=dmbl irde vyab ymhg
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=mahdilaith380@gmail.com
FRONTEND_URL=<your-frontend-url>
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=<your-frontend-url>
```

## 4. Deploy

Click "Create Web Service" and wait 5-10 minutes

## 5. Test

Visit: `https://<your-app>.onrender.com/graphql/`

## 6. Clean Up Vercel

See `CLEANUP_VERCEL.md` for detailed cleanup steps

---

For detailed instructions, see `RENDER_DEPLOYMENT.md`
