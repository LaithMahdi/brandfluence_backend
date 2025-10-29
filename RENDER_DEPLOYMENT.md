# Render Deployment Guide for Brandfluence Backend

This guide will help you deploy your Django GraphQL API to Render.

## Prerequisites

1. A GitHub account with your code pushed to a repository
2. A Render account (sign up at https://render.com)
3. A Neon PostgreSQL database (you already have this configured)

## Deployment Steps

### 1. Prepare Your Repository

Make sure all changes are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create a New Web Service on Render

1. Go to https://dashboard.render.com/
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository (LaithMahdi/brandfluence_backend)
4. Configure the service:
   - **Name**: `brandfluence-backend` (or your preferred name)
   - **Region**: Choose the closest region to your users
   - **Branch**: `main`
   - **Root Directory**: (leave blank)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn brandfluence.wsgi:application`
   - **Plan**: Free (or choose a paid plan)

### 3. Configure Environment Variables

In the Render dashboard, add the following environment variables:

#### Required Environment Variables:

1. **SECRET_KEY**

   - Value: Your Django secret key (generate a new one for production)
   - To generate: `python generate_secret_key.py`

2. **DEBUG**

   - Value: `False`

3. **DATABASE_URL**

   - Value: Your Neon PostgreSQL connection string
   - Current: `postgresql://neondb_owner:npg_l9Y2wObTsSqF@ep-still-mouse-ahqqpbr8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require`

4. **ALLOWED_HOSTS**

   - Value: Your Render URL (e.g., `brandfluence-backend.onrender.com`)
   - You can also add multiple hosts separated by commas

5. **CSRF_TRUSTED_ORIGINS**
   - Value: `https://your-render-url.onrender.com,https://your-frontend-domain.com`
   - Replace with your actual Render URL and frontend domain

#### Email Configuration:

6. **EMAIL_HOST**

   - Value: `smtp.gmail.com`

7. **EMAIL_PORT**

   - Value: `587`

8. **EMAIL_HOST_USER**

   - Value: `brandfluence@gmail.com`

9. **EMAIL_HOST_PASSWORD**

   - Value: Your Gmail app password

10. **EMAIL_USE_TLS**

    - Value: `True`

11. **DEFAULT_FROM_EMAIL**
    - Value: `mahdilaith380@gmail.com`

#### Frontend Configuration:

12. **FRONTEND_URL**
    - Value: Your frontend URL (e.g., `https://your-frontend.vercel.app`)

#### CORS Configuration:

13. **CORS_ALLOW_ALL_ORIGINS**

    - Value: `False` (for production security)

14. **CORS_ALLOWED_ORIGINS**
    - Value: `https://your-frontend-domain.com,https://another-domain.com`
    - Comma-separated list of allowed frontend origins

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Wait for the deployment to complete (first deployment may take 5-10 minutes)

### 5. Verify Deployment

Once deployed, test your API:

1. Visit: `https://your-app-name.onrender.com/graphql/`
2. You should see the GraphiQL interface
3. Try a test query to verify everything works

### 6. Update Frontend Configuration

Update your frontend to use the new Render backend URL:

- Replace Vercel URL with: `https://your-app-name.onrender.com/graphql/`

## Important Notes

### Free Tier Limitations

- Free Render services spin down after 15 minutes of inactivity
- First request after spin-down may take 30-50 seconds to respond
- Consider upgrading to a paid plan for production use

### Database Migrations

The `build.sh` script automatically runs migrations during deployment. If you need to run migrations manually:

1. Go to Render dashboard
2. Click on your web service
3. Go to "Shell" tab
4. Run: `python manage.py migrate`

### Static Files

Static files are collected automatically during build using WhiteNoise. No additional configuration needed.

### Logs

To view logs:

1. Go to your Render dashboard
2. Click on your web service
3. Go to "Logs" tab

### Custom Domain

To add a custom domain:

1. Go to your web service settings
2. Click "Custom Domain"
3. Follow the instructions to configure DNS

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure `build.sh` has proper permissions

### Database Connection Issues

- Verify `DATABASE_URL` is correctly set
- Check if Neon database is accessible
- Ensure SSL mode is properly configured

### Static Files Not Loading

- Check if `collectstatic` ran successfully in build logs
- Verify `STATIC_ROOT` and `STATIC_URL` settings
- Ensure WhiteNoise middleware is properly configured

### CORS Errors

- Add your frontend domain to `CORS_ALLOWED_ORIGINS`
- Verify `CSRF_TRUSTED_ORIGINS` includes your domains
- Check that `ALLOWED_HOSTS` includes your Render URL

## Monitoring

Render provides built-in monitoring:

- CPU and Memory usage
- Response times
- Request logs
- Error rates

Access these in your service dashboard.

## Scaling

To scale your application:

1. Upgrade from Free tier to Starter or higher
2. Configure auto-scaling rules
3. Consider adding Redis for caching
4. Use CDN for static assets

## Security Checklist

- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` (different from development)
- ✅ `ALLOWED_HOSTS` properly configured
- ✅ `CSRF_TRUSTED_ORIGINS` properly configured
- ✅ `CORS_ALLOWED_ORIGINS` with specific domains only
- ✅ Database uses SSL connection
- ✅ Environment variables stored securely in Render
- ✅ Email credentials use app-specific passwords

## Next Steps

1. Set up monitoring and alerts
2. Configure automatic deployments on git push
3. Set up staging environment
4. Configure backup strategy for database
5. Add health check endpoint
6. Set up error tracking (e.g., Sentry)

## Support

- Render Documentation: https://render.com/docs
- Django Documentation: https://docs.djangoproject.com/
- Community Support: Render Community Forum

---

**Deployment Date**: Setup for migration from Vercel to Render
**Last Updated**: October 29, 2025
