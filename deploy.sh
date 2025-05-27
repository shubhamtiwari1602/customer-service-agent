#!/bin/bash

# 🚀 Complete Deployment Script for Customer Service Agent
# This script will help you deploy to GitHub + Railway/Render

echo "🌟 Customer Service Agent - Deployment Setup"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Step 2: Initialize Git repository
echo -e "${BLUE}📁 Setting up Git repository...${NC}"

if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${YELLOW}⚠️  Git repository already exists${NC}"
fi

# Step 3: Create .gitignore
echo -e "${BLUE}📝 Creating .gitignore...${NC}"

cat > .gitignore << EOL
# Dependencies
node_modules/
backend/venv/
backend/__pycache__/
frontend/build/

# Environment variables
.env
.env.local
.env.production
.env.development

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# next.js build output
.next

# nuxt.js build output
.nuxt

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS port file
.tern-port

# macOS
.DS_Store

# PyCharm
.idea/

# VS Code
.vscode/

# Pytest cache
.pytest_cache/

# Coverage reports
htmlcov/
.coverage
coverage.xml
EOL

echo -e "${GREEN}✅ .gitignore created${NC}"

# Step 4: Install frontend dependencies
echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
cd frontend
npm install
npm install --save-dev gh-pages
cd ..
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Step 5: Create environment file template
echo -e "${BLUE}⚙️  Creating environment template...${NC}"

cat > .env.example << EOL
# Production API URL (replace with your actual deployed backend URL)
REACT_APP_API_URL=https://your-backend-app.railway.app

# Optional: Production domain for CORS
PRODUCTION_DOMAIN=https://yourusername.github.io
EOL

echo -e "${GREEN}✅ Environment template created${NC}"

# Step 6: Test local setup
echo -e "${BLUE}🧪 Testing local setup...${NC}"

cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Run quick test
python -c "import fastapi, uvicorn, pydantic, textblob; print('✅ All backend dependencies working')"

cd ..
echo -e "${GREEN}✅ Local setup verified${NC}"

# Step 7: Create deployment instructions
echo -e "${BLUE}📋 Creating deployment instructions...${NC}"

cat > DEPLOY.md << 'EOL'
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

EOL

echo -e "${GREEN}✅ Deployment instructions created${NC}"

# Step 8: Commit all changes
echo -e "${BLUE}💾 Committing changes...${NC}"

git add .
git status

echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Create GitHub repository at: https://github.com/new"
echo "2. Follow instructions in DEPLOY.md"
echo "3. Your app will be live on the internet!"
echo ""
echo -e "${BLUE}📖 Read DEPLOY.md for detailed deployment steps${NC}"
