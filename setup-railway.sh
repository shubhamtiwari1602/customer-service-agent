#!/bin/bash

echo "🔧 Setting up Railway-compatible structure..."

# Create a simple structure Railway can understand
echo "📁 Creating railway-deploy directory..."
mkdir -p railway-deploy

# Copy backend files to a Railway-friendly structure
echo "📋 Copying backend files..."
cp backend/main.py railway-deploy/
cp backend/requirements.txt railway-deploy/
cp backend/kb.md railway-deploy/

# Create Procfile for Railway
echo "📝 Creating Railway Procfile..."
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > railway-deploy/Procfile

echo ""
echo "✅ Railway deployment structure created!"
echo ""
echo "🚀 Next steps:"
echo "1. Delete your current Railway project"
echo "2. Go to railway.app"
echo "3. Create new project"
echo "4. Deploy the 'railway-deploy' folder specifically"
echo "5. Or use Railway CLI:"
echo "   cd railway-deploy"
echo "   railway login"
echo "   railway init"
echo "   railway up"
echo ""
echo "This should work without any Docker/pip issues!"
