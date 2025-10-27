# Deploy Django to Vercel

This guide will help you deploy your Brandfluence Django application to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional but recommended)
3. A PostgreSQL database (recommended: Neon, Supabase, or Railway)

## Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

## Step 2: Configure Environment Variables

Before deploying, you need to set up environment variables in Vercel. Go to your Vercel project settings and add these:

### Required Environment Variables

```
# Django Settings
SECRET_KEY=your-very-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=.vercel.app,your-custom-domain.com

# Database (Use PostgreSQL for production)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# CORS (Add your frontend URLs)
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-domain.com
```

### Optional Environment Variables

```
# Email Configuration (for password reset, etc.)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Step 3: Set Up PostgreSQL Database

**Option A: Use Neon (Recommended)**

1. Go to https://neon.tech
2. Create a free account
3. Create a new project
4. Copy the connection string
5. Add it to Vercel as `DATABASE_URL`

**Option B: Use Supabase**

1. Go to https://supabase.com
2. Create a project
3. Go to Settings → Database
4. Copy the connection string (use connection pooling)
5. Add it to Vercel as `DATABASE_URL`

**Option C: Use Railway**

1. Go to https://railway.app
2. Create a PostgreSQL database
3. Copy the connection string
4. Add it to Vercel as `DATABASE_URL`

## Step 4: Update CORS Settings (Production)

In `settings.py`, update CORS for production:

```python
# Get CORS origins from environment variable
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# For production, set this to False
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False') == 'True'
```

Add to Vercel environment variables:

```
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://yourdomain.com
CORS_ALLOW_ALL_ORIGINS=False
```

## Step 5: Deploy to Vercel

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Import your Git repository (GitHub, GitLab, or Bitbucket)
3. Select your repository
4. Configure project:
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as is)
   - Build Command: Leave empty
   - Output Directory: Leave empty
5. Add environment variables (see Step 2)
6. Click **Deploy**

### Method 2: Deploy via Vercel CLI

```bash
# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? brandfluence-backend
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

## Step 6: Run Database Migrations

After deployment, you need to run migrations on your production database.

### Option 1: Via Vercel CLI

```bash
vercel env pull .env.production
python manage.py migrate --settings=brandfluence.settings
```

### Option 2: Via Railway/Render (if using managed Django hosting)

Set up a one-off command to run migrations.

### Option 3: Create a management endpoint (NOT RECOMMENDED for production)

Only use this temporarily and remove after migrations.

## Step 7: Create Superuser

You need to create a superuser for your production database.

### Option 1: Using Django shell locally with production DB

```bash
# Export production DATABASE_URL
export DATABASE_URL=your-production-database-url

# Run Django shell
python manage.py shell

# In the shell:
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser(
    email='admin@yourdomain.com',
    name='Admin User',
    password='your-secure-password'
)
```

### Option 2: Create a temporary management command

Create `users/management/commands/createsuperuser_automated.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PASSWORD')
        name = os.getenv('ADMIN_NAME', 'Admin')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                name=name,
                password=password
            )
            self.stdout.write(f'Superuser {email} created!')
```

Then run locally with production DB connection.

## Step 8: Test Your Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app/graphql/`
2. You should see the GraphQL playground
3. Test login mutation:

```graphql
mutation {
  tokenAuth(email: "admin@yourdomain.com", password: "your-password") {
    token
    user {
      email
      name
    }
  }
}
```

## Step 9: Set Up Custom Domain (Optional)

1. Go to your Vercel project settings
2. Click **Domains**
3. Add your custom domain
4. Follow the DNS configuration instructions
5. Update `ALLOWED_HOSTS` in environment variables

## Troubleshooting

### Issue: "DisallowedHost at /"

**Solution:** Add your Vercel domain to `ALLOWED_HOSTS` environment variable:

```
ALLOWED_HOSTS=.vercel.app,your-project.vercel.app
```

### Issue: "Database connection failed"

**Solution:**

- Verify `DATABASE_URL` is correct
- Ensure your database allows connections from Vercel IPs
- For Neon, enable IP allowlist bypass or add Vercel IPs

### Issue: "Static files not loading"

**Solution:**

- Run `python manage.py collectstatic` locally
- Commit the `staticfiles_build` directory
- Or use a CDN for static files

### Issue: "CORS errors from frontend"

**Solution:**

- Add your frontend URL to `CORS_ALLOWED_ORIGINS`
- Set `CORS_ALLOW_CREDENTIALS=True` in environment variables

### Issue: "Module not found"

**Solution:**

- Ensure all dependencies are in `requirements.txt`
- Check Vercel build logs for errors

## Important Notes

### Limitations on Vercel

- **Serverless functions timeout**: 10 seconds (Hobby), 60 seconds (Pro)
- **No persistent file storage**: Use cloud storage for media files
- **Read-only file system**: Can't write to disk (except /tmp)
- **Cold starts**: First request may be slow

### Recommendations

1. Use PostgreSQL, not SQLite in production
2. Use cloud storage (AWS S3, Cloudinary) for media files
3. Enable database connection pooling
4. Set appropriate timeout values
5. Monitor your Vercel usage and logs

## Production Checklist

- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] PostgreSQL database configured
- [ ] `ALLOWED_HOSTS` properly set
- [ ] CORS origins restricted
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Environment variables secured
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] Error monitoring set up (optional: Sentry)
- [ ] Backup strategy in place

## Continuous Deployment

Vercel automatically deploys when you push to your Git repository:

- Push to `main` branch → Production deployment
- Push to other branches → Preview deployment
- Pull requests → Automatic preview deployments

## Monitoring and Logs

View logs in Vercel dashboard:

1. Go to your project
2. Click **Deployments**
3. Select a deployment
4. View **Function Logs**

## Next Steps

1. Set up monitoring (Sentry, etc.)
2. Configure email for password reset
3. Set up automated backups for database
4. Add CI/CD tests
5. Configure custom domain
6. Set up staging environment

## Support

- Vercel Docs: https://vercel.com/docs
- Django on Vercel: https://vercel.com/guides/deploying-django-with-vercel
- Neon Database: https://neon.tech/docs

## Environment Variables Summary

Copy this template to your Vercel project settings:

```env
# Django Core
SECRET_KEY=your-secret-key-generate-new-one
DEBUG=False
ALLOWED_HOSTS=.vercel.app

# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOW_CREDENTIALS=True
```
