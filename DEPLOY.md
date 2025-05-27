# 🚀 Quick Deployment Instructions

## Step 1: Create GitHub Repository

1. Go to GitHub.com and create a new repository named `customer-service-agent`
2. Don't initialize with README (we have files already)

## Step 2: Push to GitHub

```bash
git add .
git commit -m "Initial commit: Customer Service Agent"
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/customer-service-agent.git
git push -u origin main
```

## Step 3: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `customer-service-agent` repository
4. Choose "Deploy from a folder" → select `backend`
5. Railway will auto-detect Python and deploy using the Procfile
6. Copy your app URL (e.g., `https://your-app.railway.app`)

## Step 4: Update Frontend Configuration

1. Edit `frontend/src/App.js`:
   - Replace `https://your-api-domain.railway.app` with your actual Railway URL
2. Edit `frontend/package.json`:
   - Replace `yourusername` with your GitHub username

## Step 5: Deploy Frontend to GitHub Pages

```bash
cd frontend
npm run deploy
```

## Step 6: Enable GitHub Pages

1. Go to your GitHub repository
2. Settings → Pages
3. Source: "Deploy from a branch"
4. Branch: `gh-pages` → `/root`
5. Save

## 🎉 Your app will be live at:

- **Frontend**: `https://yourusername.github.io/customer-service-agent`
- **Backend**: `https://your-app.railway.app`

## Alternative: Deploy Backend to Render

1. Go to [render.com](https://render.com)
2. Connect GitHub repository
3. Create "Web Service" from `backend` folder
4. Use the `render.yaml` configuration provided

