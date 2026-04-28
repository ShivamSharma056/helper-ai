# Vercel Deployment Guide

## Quick Deploy to Vercel

1. **Fork/Clone this repository** to your GitHub account

2. **Go to Vercel**: https://vercel.com/
   - Click "New Project"
   - Import your GitHub repository
   - Connect your GitHub account
   - Select this repository

3. **Vercel will auto-detect** your Python app and deploy it

4. **Set Environment Variables** in Vercel dashboard:
   - `ANTHROPIC_API_KEY` = Your Anthropic API key
   - `SECRET_KEY` = Any random string (for session security)

5. **Your app will be live** at `https://your-project-name.vercel.app`

## Manual Setup (if auto-deploy fails)

If Vercel doesn't auto-detect, configure in the project settings:

- **Framework Preset**: Python
- **Root Directory**: `/`
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: `.`

## Testing Your Deployment

After deployment, test these URLs:
- `https://your-app.vercel.app/` - Landing page
- `https://your-app.vercel.app/login` - Login page

## Troubleshooting

- **WebSocket issues**: Vercel supports WebSockets in serverless functions, but check your plan
- **Database**: SQLite works fine, data persists between deploys
- **Static files**: Served automatically by Flask