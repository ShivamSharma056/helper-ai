# Helper.ai 🤖

Intelligent study assistant — AI-powered PPT, Reports, Smart Notes with real-time collaboration.

## Tech Stack
- **Backend**: Python · Flask · Flask-SocketIO · Flask-SQLAlchemy · Flask-Bcrypt
- **AI**: Anthropic Claude (claude-sonnet-4-20250514)
- **Database**: SQLite (dev) — swap to PostgreSQL for production
- **Real-time**: Socket.IO (WebSockets)
- **Frontend**: Vanilla JS · HTML · CSS (no framework needed)

## Project Structure
```
helperai/
├── app.py            ← Flask app, routes, Socket.IO events
├── db.py             ← SQLAlchemy models (User, Document, SharedDocument)
├── ai_engine.py      ← Anthropic API calls (PPT / Report / Notes)
├── requirements.txt
├── templates/
│   ├── index.html    ← Landing page
│   ├── login.html    ← Auth page (login + register tabs)
│   └── dashboard.html← Main app
└── static/
    ├── css/style.css ← Full stylesheet (dark mode included)
    └── js/app.js     ← All frontend logic + Socket.IO client
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
**Important**: You need an Anthropic API key, not OpenAI!

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up for a free account
3. Create an API key (it will start with `sk-ant-`)
4. Copy the key to your `.env` file:

```bash
# Edit the .env file (not .env.example!)
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
```

**❌ Don't use OpenAI keys** - They start with `sk-proj-` and won't work with Anthropic.

Get your key at: https://console.anthropic.com

### 3. Run the app
```bash
python app.py
```

### Quick Setup Scripts

**For API Key Setup (Recommended):**
```bash
setup_api_key_v2.bat
```

**For Full Setup:**
```bash
setup.bat
```

## 🚀 Deployment

### Quick Deploy with Scripts

**For Linux/Mac:**
```bash
./deploy.sh
```

**For Windows:**
```cmd
deploy.bat
```

### Manual Deployment to Railway (Recommended - Free & Easy)
1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **Connect GitHub**: Link your GitHub repository
3. **Deploy**: Railway will automatically detect Flask and deploy
4. **Set Environment Variables**:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `SECRET_KEY`: A random secret key (generate one)
5. **Get Your URL**: Railway provides a `*.up.railway.app` domain

### Render (Alternative Free Option)
1. **Create Render Account**: Go to [render.com](https://render.com)
2. **Connect Repository**: Link your GitHub repo
3. **Configure Service**:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --worker-class eventlet -w 1 app:app`
4. **Set Environment Variables**: Same as Railway
5. **Deploy**: Get your `*.onrender.com` URL

### Heroku (Classic Option)
1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create App**: `heroku create your-app-name`
4. **Set Environment Variables**:
   ```bash
   heroku config:set ANTHROPIC_API_KEY=your-key-here
   heroku config:set SECRET_KEY=your-secret-here
   ```
5. **Deploy**: `git push heroku main`
6. **Open**: `heroku open`

## 🐛 Troubleshooting

### "Network error. Try again." when generating content

**Cause**: Missing Anthropic API key or not logged in.

**Solutions**:

1. **Set API Key** (Required for AI features):
   ```bash
   # Windows
   set ANTHROPIC_API_KEY=your-api-key-here

   # Linux/Mac
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

2. **Get API Key**: Visit [console.anthropic.com](https://console.anthropic.com) and create an account

3. **For deployed apps**: Set `ANTHROPIC_API_KEY` in your hosting platform's environment variables

4. **Make sure you're logged in**: The generate buttons require authentication

### "Unauthorized" errors

- Clear your browser cookies and log in again
- Your session may have expired

### Database errors

- Delete `instance/helperai.db` and restart the app to recreate the database
- Make sure the app has write permissions to the `instance/` folder

### WebSocket connection issues

- Real-time collaboration requires WebSocket support
- Some hosting platforms may not support WebSockets in free tiers

Open http://localhost:5000 in your browser.

## Features
| Feature | Status |
|---------|--------|
| User registration & login (bcrypt) | ✅ |
| Auto PPT Maker (8-12 slides + notes) | ✅ |
| Report Generator (7 sections) | ✅ |
| Smart Notes + Flashcards | ✅ |
| Voice input (Web Speech API) | ✅ |
| Real-time collaborative editing | ✅ |
| Private / encrypted documents | ✅ |
| Shareable document links | ✅ |
| Cloud file management | ✅ |
| Dark mode (auto) | ✅ |
| Mobile responsive | ✅ |

## Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | *(required)* | Your Anthropic API key |
| `SECRET_KEY` | `helperai-secret-2025` | Flask session secret — change in production! |

## Production Deployment
1. Replace `sqlite:///helperai.db` with a PostgreSQL URL in `app.config`
2. Set a strong `SECRET_KEY` environment variable
3. Run with gunicorn: `gunicorn -k eventlet -w 1 app:app`

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Create account |
| POST | `/api/login` | Sign in |
| POST | `/api/logout` | Sign out |
| GET  | `/api/me` | Current user info |
| POST | `/api/generate/ppt` | Generate presentation |
| POST | `/api/generate/report` | Generate report |
| POST | `/api/generate/notes` | Generate smart notes |
| GET  | `/api/documents` | List user documents |
| GET  | `/api/documents/:id` | Get single document |
| POST | `/api/documents/:id/share` | Create share link |
| DELETE | `/api/documents/:id` | Delete document |
| GET  | `/shared/:token` | View shared document |

## Socket.IO Events
| Event | Direction | Description |
|-------|-----------|-------------|
| `join_room` | Client → Server | Join collaboration room |
| `leave_room` | Client → Server | Leave room |
| `note_update` | Client → Server | Broadcast note changes |
| `note_changed` | Server → Client | Receive note changes |
| `user_joined` | Server → Client | Someone joined room |
| `user_left` | Server → Client | Someone left room |
