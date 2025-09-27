#!/bin/bash

# Ekavarta Setup Script
# This script helps set up the development environment and handles large files

echo "🚀 Ekavarta Setup Script"
echo "========================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

if ! command_exists git; then
    echo "❌ Git is not installed. Please install Git."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version is too old. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ All prerequisites met!"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the Ekavarta root directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install server dependencies"
    exit 1
fi

cd client
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install client dependencies"
    exit 1
fi
cd ..

echo "✅ Dependencies installed successfully!"

# Setup environment file
echo "🔧 Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "ℹ️  .env file already exists"
fi

# Check for Git LFS
echo "📦 Checking Git LFS setup..."
if command_exists git-lfs; then
    git lfs install
    echo "✅ Git LFS is set up"
else
    echo "⚠️  Git LFS not found. Install it for large file support:"
    echo "   - Ubuntu/Debian: apt install git-lfs"
    echo "   - macOS: brew install git-lfs"
    echo "   - Windows: Download from https://git-lfs.github.io/"
fi

# Check repository size
echo "📊 Checking repository size..."
REPO_SIZE=$(du -sh .git | cut -f1)
echo "Repository size: $REPO_SIZE"

# Find large files
echo "🔍 Checking for large files..."
LARGE_FILES=$(find . -type f -size +10M -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./client/node_modules/*" 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo "⚠️  Found large files (>10MB):"
    echo "$LARGE_FILES" | while read -r file; do
        SIZE=$(du -sh "$file" | cut -f1)
        echo "   $file ($SIZE)"
    done
    echo "💡 Consider using Git LFS for these files. Run: npm run lfs:install"
else
    echo "✅ No large files found"
fi

# Test build
echo "🏗️  Testing build process..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

echo "✅ Build successful!"

# Create uploads directory
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo "✅ Created uploads directory"
fi

# Final instructions
echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Edit .env file with your configuration:"
echo "   - MongoDB URI"
echo "   - JWT Secret"
echo "   - API keys"
echo ""
echo "2. Start development server:"
echo "   npm run dev"
echo ""
echo "3. For production deployment, see:"
echo "   - DEPLOYMENT.md for hosting options"
echo "   - LARGE_FILES_GUIDE.md for large file management"
echo ""
echo "4. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:5000"
echo "   - Health check: http://localhost:5000/api/health"
echo ""

# Check for common issues
if [ ! -d "node_modules" ] || [ ! -d "client/node_modules" ]; then
    echo "⚠️  Warning: node_modules directory missing. Run 'npm install' again."
fi

if [ -d "client/build" ]; then
    BUILD_SIZE=$(du -sh client/build | cut -f1)
    echo "📦 Client build size: $BUILD_SIZE"
fi

echo "Happy coding! 🚀"