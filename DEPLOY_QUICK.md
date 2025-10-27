# Quick Deploy to Vercel

## 🚀 Quick Start (5 minutes)

### 1. Push to GitHub

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 2. Import to Vercel

1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Click **Deploy** (no configuration needed)

### 3. Add Environment Variables

Go to your Vercel project → Settings → Environment Variables and add:

```
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=.vercel.app
DATABASE_URL=postgresql://user:password@host:port/database
```

### 4. Redeploy

Click **Redeploy** in Vercel dashboard

### 5. Access Your API

Your GraphQL API will be available at:

```
https://your-project.vercel.app/graphql/
```

## 📊 Database Setup (Choose One)

### Option A: Neon (Free, Recommended)

1. Go to https://neon.tech → Sign up
2. Create new project
3. Copy connection string
4. Add to Vercel as `DATABASE_URL`

### Option B: Supabase (Free)

1. Go to https://supabase.com → New project
2. Settings → Database → Connection string
3. Copy URI (connection pooling)
4. Add to Vercel as `DATABASE_URL`

## ✅ Test Your Deployment

```graphql
# Open https://your-project.vercel.app/graphql/

mutation {
  tokenAuth(email: "test@example.com", password: "password") {
    token
  }
}
```

## 🔧 Common Issues

**"DisallowedHost"**
→ Add your domain to `ALLOWED_HOSTS` env var

**Database errors**
→ Verify `DATABASE_URL` is correct

**CORS errors**
→ Add frontend URL to `CORS_ALLOWED_ORIGINS`

## 📚 Full Documentation

See `VERCEL_DEPLOYMENT.md` for detailed instructions.
