# Vercel Deployment Configuration

## Environment Variables
For the Vercel deployment to work properly, add the following environment variable in your Vercel project dashboard:

**Variable Name:** `REACT_APP_API_URL`
**Value:** `https://customer-service-agent-api.onrender.com`

## Deployment Steps
1. ✅ Fixed package.json - Removed conflicting homepage field
2. ✅ Added vercel.json for proper routing configuration  
3. ✅ Created .env.production for API URL (local only)
4. ✅ Pushed changes to GitHub (triggers auto-deploy)

## Manual Vercel Setup (if needed)
If automatic deployment doesn't work:

1. Go to https://vercel.com/dashboard
2. Import your GitHub repository
3. Set Framework Preset to "Create React App"
4. Set Root Directory to "frontend"
5. Add environment variable: REACT_APP_API_URL = https://customer-service-agent-api.onrender.com
6. Deploy

## Vercel Project URL
Your Vercel deployment should be accessible at:
https://customer-service-agent-black.vercel.app

## Testing
After deployment, test the following features:
- ✅ Page loads without blank screen
- ✅ Query classification works
- ✅ Sentiment analysis displays
- ✅ API calls to backend succeed
- ✅ All UI components render properly
