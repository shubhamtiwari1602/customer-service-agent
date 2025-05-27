#!/bin/bash

# GitHub Pages Deployment Script
# Run this after you've created the GitHub repository and pushed your code

echo "🚀 Customer Service Agent - GitHub Pages Deployment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if GitHub remote is set up
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Error: No GitHub remote found. Please set up your GitHub repository first."
    echo "   Follow the instructions in CREATE_GITHUB_REPO.md"
    exit 1
fi

echo "📦 Installing frontend dependencies..."
cd frontend
npm install

echo "🔧 Building frontend for production..."
npm run build

echo "🌐 Deploying to GitHub Pages..."
npm run deploy

echo "✅ Deployment complete!"
echo ""
echo "Your customer service agent is now live at:"
echo "https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1.github.io\/\2/')/"
echo ""
echo "🔗 Next steps:"
echo "1. Deploy your backend to Railway.app (see DEPLOYMENT_GUIDE.md)"
echo "2. Update the API URL in frontend/src/App.js with your Railway URL"
echo "3. Run this script again to redeploy with the correct backend URL"
