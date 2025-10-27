# 🚀 Vercel Deployment Checklist

## Pre-Deployment

- [ ] Code is committed to Git
- [ ] All changes pushed to GitHub/GitLab/Bitbucket
- [ ] PostgreSQL database is set up (Neon/Supabase/Railway)
- [ ] Generated new SECRET_KEY using `python generate_secret_key.py`

## Vercel Setup

- [ ] Created Vercel account
- [ ] Imported repository to Vercel
- [ ] First deployment completed

## Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

### Required ✅

- [ ] `SECRET_KEY` - New secret key (from generate_secret_key.py)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `DEBUG` - Set to `False`
- [ ] `ALLOWED_HOSTS` - `.vercel.app` or your domain

### Recommended 👍

- [ ] `CORS_ALLOW_ALL_ORIGINS` - Set to `False`
- [ ] `CORS_ALLOWED_ORIGINS` - Your frontend URL(s)
- [ ] `CORS_ALLOW_CREDENTIALS` - Set to `True`

## Database Setup

- [ ] PostgreSQL database created
- [ ] DATABASE_URL copied to Vercel
- [ ] Local environment connected to production DB
- [ ] Migrations run: `python manage.py migrate`
- [ ] Superuser created: `python manage.py createsuperuser`

## Post-Deployment Testing

- [ ] Visit GraphQL endpoint: `https://your-project.vercel.app/graphql/`
- [ ] GraphQL Playground loads successfully
- [ ] Test user registration mutation
- [ ] Test login mutation (tokenAuth)
- [ ] Test authenticated query (me)
- [ ] Admin panel accessible: `https://your-project.vercel.app/admin/`
- [ ] Can login to admin with superuser

## Security Verification

- [ ] `DEBUG=False` in production
- [ ] Strong SECRET_KEY is set
- [ ] ALLOWED_HOSTS properly configured
- [ ] CORS properly restricted
- [ ] Database credentials secured
- [ ] No sensitive data in version control
- [ ] HTTPS enabled (automatic on Vercel)

## Optional Enhancements

- [ ] Custom domain configured
- [ ] Frontend connected and CORS working
- [ ] Error monitoring (Sentry) set up
- [ ] Database backups configured
- [ ] CI/CD pipeline set up
- [ ] Staging environment created

## Documentation

- [ ] Team knows how to access admin panel
- [ ] API documentation shared
- [ ] Environment variables documented
- [ ] Deployment process documented

## Maintenance

- [ ] Monitor Vercel logs regularly
- [ ] Set up alerts for errors
- [ ] Plan database backup strategy
- [ ] Review and update dependencies

---

## Quick Commands

### Generate Secret Key

```bash
python generate_secret_key.py
```

### Run Migrations (with production DB)

```bash
# Set DATABASE_URL first
python manage.py migrate
```

### Create Superuser (with production DB)

```bash
python manage.py createsuperuser
```

### Test Login

```graphql
mutation {
  tokenAuth(email: "your-email@example.com", password: "your-password") {
    token
    user {
      id
      email
      name
    }
  }
}
```

---

## Troubleshooting

### Issue: DisallowedHost Error

**Fix**: Add domain to `ALLOWED_HOSTS` environment variable

### Issue: Database Connection Failed

**Fix**: Verify `DATABASE_URL` is correct and database is accessible

### Issue: CORS Errors

**Fix**: Add frontend URL to `CORS_ALLOWED_ORIGINS`

### Issue: Static Files Not Loading

**Fix**: Run `python manage.py collectstatic --noinput`

---

## Support Resources

- 📖 Full Guide: `VERCEL_DEPLOYMENT.md`
- ⚡ Quick Start: `DEPLOY_QUICK.md`
- 📝 Summary: `DEPLOYMENT_SUMMARY.md`
- 🔐 Authentication: `users/AUTHENTICATION.md`
- 💻 Code Examples: `users/AUTH_EXAMPLES.md`

---

**Last Updated**: October 27, 2025
**Project**: Brandfluence Backend
**Framework**: Django 5.2.7 + GraphQL
