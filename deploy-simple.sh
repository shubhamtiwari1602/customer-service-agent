#!/bin/bash

# Simple deployment script for Railway + Vercel/Netlify
echo "🚀 Deploying Customer Service Agent"
echo "==================================="

# Get current directory
PROJECT_DIR=$(pwd)

echo "📂 Project directory: $PROJECT_DIR"

# Check if we're in the right place
if [ ! -f "frontend/package.json" ] || [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Make sure you have both frontend/ and backend/ folders"
    exit 1
fi

# Deploy backend to Railway
echo ""
echo "🔧 Step 1: Deploy Backend to Railway"
echo "------------------------------------"
echo "1. Go to https://railway.app"
echo "2. Connect your GitHub account"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your repository"
echo "5. Railway will auto-detect the backend and deploy it"
echo "6. Copy your Railway URL (e.g., https://web-production-xxxx.up.railway.app)"
echo ""
read -p "✅ Have you deployed to Railway and copied the URL? (y/n): " railway_done

if [ "$railway_done" != "y" ]; then
    echo "Please complete the Railway deployment first, then run this script again."
    exit 1
fi

# Get Railway URL from user
echo ""
read -p "🔗 Enter your Railway backend URL (e.g., https://web-production-xxxx.up.railway.app): " railway_url

if [ -z "$railway_url" ]; then
    echo "❌ Railway URL is required"
    exit 1
fi

# Update frontend with Railway URL
echo ""
echo "🔧 Step 2: Update Frontend Configuration"
echo "----------------------------------------"

# Update the API URL in the frontend
cd frontend
sed -i.bak "s|https://your-api-domain.railway.app|$railway_url|g" src/App.js
echo "✅ Updated frontend API URL to: $railway_url"

# Build the frontend
echo ""
echo "📦 Building frontend..."
npm install
npm run build

echo ""
echo "🌐 Step 3: Deploy Frontend"
echo "--------------------------"
echo "Choose your preferred hosting platform:"
echo "1. Vercel (Recommended - easiest)"
echo "2. Netlify"
echo "3. GitHub Pages"
echo ""

read -p "Enter your choice (1, 2, or 3): " hosting_choice

case $hosting_choice in
    1)
        echo ""
        echo "🚀 Deploying to Vercel..."
        echo "1. Go to https://vercel.com"
        echo "2. Sign up/login with GitHub"
        echo "3. Click 'New Project'"
        echo "4. Import your repository"
        echo "5. Set Framework Preset to 'Create React App'"
        echo "6. Set Root Directory to 'frontend'"
        echo "7. Click 'Deploy'"
        echo ""
        echo "Your app will be live at: https://your-repo-name.vercel.app"
        ;;
    2)
        echo ""
        echo "🚀 Deploying to Netlify..."
        echo "1. Go to https://netlify.com"
        echo "2. Sign up/login with GitHub"
        echo "3. Click 'New site from Git'"
        echo "4. Choose your repository"
        echo "5. Set Base directory to 'frontend'"
        echo "6. Set Build command to 'npm run build'"
        echo "7. Set Publish directory to 'frontend/build'"
        echo "8. Click 'Deploy site'"
        echo ""
        echo "Your app will be live at: https://random-name.netlify.app"
        ;;
    3)
        echo ""
        echo "🚀 Deploying to GitHub Pages..."
        # Get GitHub username
        github_url=$(git config --get remote.origin.url 2>/dev/null || echo "")
        if [[ $github_url == *github.com* ]]; then
            username=$(echo $github_url | sed 's/.*github.com[:/]\([^/]*\)\/.*/\1/')
            repo=$(echo $github_url | sed 's/.*\/\([^.]*\).*/\1/')
            
            # Update package.json with correct homepage
            sed -i.bak "s|https://yourusername.github.io/customer-service-agent|https://$username.github.io/$repo|g" package.json
            
            echo "✅ Updated homepage URL to: https://$username.github.io/$repo"
            
            # Deploy to GitHub Pages
            npm run deploy
            
            echo ""
            echo "✅ Deployed to GitHub Pages!"
            echo "Your app will be live at: https://$username.github.io/$repo"
        else
            echo "❌ Could not detect GitHub repository. Please set up GitHub remote first."
        fi
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Go back to project root
cd ..

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "🔗 Your Customer Service Agent URLs:"
echo "   Backend API: $railway_url"
echo "   API Docs: $railway_url/docs"

if [ "$hosting_choice" = "3" ] && [[ $github_url == *github.com* ]]; then
    echo "   Frontend: https://$username.github.io/$repo"
fi

echo ""
echo "🧪 Test your deployment:"
echo "1. Visit your frontend URL"
echo "2. Try different types of queries:"
echo "   - Technical: 'My API is not working'"
echo "   - Feature: 'Add dark mode please'"
echo "   - Sales: 'What are your pricing plans?'"
echo "3. Verify sentiment analysis and escalation work"
echo ""
echo "💡 Share these URLs to showcase your work!"
