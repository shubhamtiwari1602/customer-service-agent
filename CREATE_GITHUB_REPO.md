# Create GitHub Repository - Step by Step

## Step 1: Create Repository on GitHub

1. Go to https://github.com and sign in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Fill in the repository details:
   - **Repository name**: `customer-service-agent`
   - **Description**: `AI-powered customer service agent with FastAPI backend and React frontend`
   - **Visibility**: Public (required for free GitHub Pages)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

4. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/customer-service-agent.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Deploy Backend to Railway

1. Go to https://railway.app and sign up/sign in
2. Click "New Project" > "Deploy from GitHub repo"
3. Select your `customer-service-agent` repository
4. Railway will automatically detect the backend and deploy it
5. Copy the deployment URL (e.g., `https://your-app.railway.app`)

## Step 4: Update Frontend with Backend URL

Once you have the Railway backend URL, update the frontend:

1. Edit `frontend/src/App.js`
2. Replace the `PRODUCTION_API_URL` with your actual Railway URL
3. Commit and push the changes

## Step 5: Deploy Frontend to GitHub Pages

After updating the frontend with the backend URL:

```bash
cd frontend
npm run deploy
```

This will deploy your frontend to: `https://YOUR_USERNAME.github.io/customer-service-agent`

## Step 6: Update package.json homepage

Update the homepage URL in `frontend/package.json` with your actual GitHub username.

---

**Your deployed application will be live at:**
- Frontend: `https://YOUR_USERNAME.github.io/customer-service-agent`
- Backend API: `https://your-app.railway.app`

The system will be fully functional and accessible from anywhere on the internet!
