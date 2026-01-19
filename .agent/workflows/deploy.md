---
description: Deploy the Django app to Railway
---

# Deploy to Railway

## Prerequisites
- Railway CLI installed (`npm install -g @railway/cli`)
- Railway account (https://railway.app)

## First-Time Setup
1. Login to Railway CLI:
```bash
railway login
```

2. Link your project (run from project root):
```bash
railway link
```

3. Set required environment variables on Railway dashboard:
   - `SECRET_KEY` - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `RAILWAY_STATIC_URL` - Set to `/static/`

## Deploy

// turbo
1. Deploy to Railway:
```bash
railway up
```

## Post-Deploy
2. Run migrations (first deploy only):
```bash
railway run python manage.py migrate
```

3. Collect static files (if needed):
```bash
railway run python manage.py collectstatic --noinput
```

## View Logs
```bash
railway logs
```

## Open Deployed App
```bash
railway open
```
