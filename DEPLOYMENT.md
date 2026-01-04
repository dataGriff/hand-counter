# Free Deployment Guide for Hand Counter

This guide provides step-by-step instructions for deploying the Hand Counter web application for free on various platforms.

## Quick Comparison

| Platform | Free Tier | Setup Difficulty | Best For |
|----------|-----------|------------------|----------|
| **Render** | ✅ 750 hours/month | ⭐ Easy | Recommended - Best overall |
| **Railway** | ✅ $5 credit/month | ⭐ Easy | Quick deployments |
| **Fly.io** | ✅ 3 VMs free | ⭐⭐ Moderate | Global edge deployment |
| **PythonAnywhere** | ✅ Limited | ⭐⭐ Moderate | Python-focused hosting |
| **Heroku** | ❌ No longer free | ⭐ Easy | (Not recommended) |

## Recommended: Render (Easiest & Best Free Tier)

**Why Render?** Free tier includes 750 hours/month, automatic deployments from GitHub, and HTTPS included.

### Step-by-Step Deployment on Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a `render.yaml` file** in your repository root:

```yaml
services:
  - type: web
    name: hand-counter
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

3. **Connect your GitHub repository:**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the `hand-counter-` repository
   - Render will auto-detect the settings from `render.yaml`

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for build and deployment
   - Your app will be live at `https://hand-counter-xxxx.onrender.com`

**Note:** Free tier services spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

## Option 2: Railway (Great for Quick Deployments)

**Why Railway?** $5 free credit per month, simple deployment, good for testing.

### Deployment Steps

1. **Sign up** at [railway.app](https://railway.app)

2. **Create a `Procfile`** in your repository:

```
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

3. **Deploy:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and installs dependencies
   - Click "Deploy"

4. **Generate domain:**
   - Go to Settings → "Generate Domain"
   - Your app will be live at `https://your-app.up.railway.app`

## Option 3: Fly.io (For Global Edge Deployment)

**Why Fly.io?** Run apps close to users globally, 3 VMs free, includes Postgres if needed.

### Deployment Steps

1. **Install Fly CLI:**
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login:**
```bash
fly auth login
```

3. **Create a `fly.toml` file:**
```toml
app = "hand-counter"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

4. **Deploy:**
```bash
fly launch
fly deploy
```

Your app will be at `https://hand-counter.fly.dev`

## Option 4: PythonAnywhere (Python-Specific Hosting)

**Why PythonAnywhere?** Free tier specifically for Python apps, includes MySQL database.

### Deployment Steps

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your code:**
   - Use the Files tab or git clone:
   ```bash
   git clone https://github.com/dataGriff/hand-counter-.git
   cd hand-counter-
   pip install --user -r requirements.txt
   ```

3. **Configure Web App:**
   - Go to Web tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.11
   - Set source code directory to `/home/yourusername/hand-counter-`
   - Edit WSGI file:
   ```python
   import sys
   path = '/home/yourusername/hand-counter-'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

4. **Reload web app** - Your app will be at `https://yourusername.pythonanywhere.com`

**Note:** Free tier has daily CPU quota limits and slower performance.

## Alternative: Docker on Free VMs

If you have more technical skills, you can deploy on free VM providers:

### Oracle Cloud (Always Free Tier)

- 2 AMD VMs with 1GB RAM each (forever free)
- Requires credit card for verification
- Full control over the VM

```bash
# On your Oracle Cloud VM
git clone https://github.com/dataGriff/hand-counter-.git
cd hand-counter-
docker build -t hand-counter .
docker run -d -p 80:8000 hand-counter
```

### Google Cloud Run (Free Tier)

- 2 million requests per month free
- Automatic scaling to zero
- Requires credit card

```bash
gcloud run deploy hand-counter \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Performance Tips for Free Tiers

1. **Keep services warm:**
   - Use a free uptime monitor like [UptimeRobot](https://uptimerobot.com) to ping your app every 5 minutes
   - Prevents cold starts on Render

2. **Optimize for slow startups:**
   - Free tiers have slower CPUs
   - Consider reducing Gunicorn workers to 2 on free plans

3. **Monitor usage:**
   - Most platforms show usage dashboards
   - Stay within limits to avoid charges

## Cost Considerations

All these options are free for personal projects with moderate traffic:

- **Render**: 750 hours/month = ~31 days if app always runs
- **Railway**: $5 credit ≈ 500 hours based on usage
- **Fly.io**: 3 shared VMs, 160GB transfer included
- **PythonAnywhere**: CPU seconds per day limited

For production apps with high traffic, consider upgrading to paid tiers (~$7-20/month).

## Recommended Setup

**Best for beginners:** Render with GitHub integration
- Automatic deploys on every push
- Free HTTPS
- Easy custom domain setup
- No credit card required

**Best for developers:** Railway or Fly.io
- More control and features
- Better performance
- Good CLI tools

## Need Help?

- Check platform documentation
- Join their Discord/Slack communities
- All platforms have extensive free tier documentation

---

**Pro Tip:** Start with Render. It's the easiest and most reliable free option. You can always migrate later if needed.
