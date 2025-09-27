# ⚡ Quick Start Guide - Ekavarta

Get your Ekavarta application running in minutes!

## 🚀 One-Command Setup

```bash
# Run the automated setup script
./scripts/setup.sh
```

This script will:
- ✅ Check prerequisites (Node.js, npm, Git)
- ✅ Install all dependencies
- ✅ Create environment file
- ✅ Set up Git LFS for large files
- ✅ Test build process
- ✅ Check for large files

## 📋 Manual Setup (if needed)

### 1. Prerequisites
- Node.js 16+ 
- npm or yarn
- Git
- MongoDB (local or cloud)

### 2. Clone & Install
```bash
git clone https://github.com/GaneshG9/Ekavarta-.git
cd Ekavarta-
npm run install-all
```

### 3. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Start Development
```bash
npm run dev
```

## 🌐 For Large Files (2GB+ Repository)

If your repository contains large files:

### Option 1: Git LFS (Recommended)
```bash
# Install Git LFS
git lfs install

# Track large files (already configured)
git lfs track

# Add and commit large files
git add .
git commit -m "Add large files with LFS"
git push origin main
```

### Option 2: External Storage
Use cloud storage services:
- **AWS S3** - Best for scalability
- **Cloudinary** - Great for images/videos
- **Google Cloud Storage** - Good integration
- **Azure Blob Storage** - Enterprise option

### Option 3: Repository Splitting
Split large repository into smaller ones:
```bash
# Main app
ekavarta-core/

# Large assets
ekavarta-assets/

# Documentation
ekavarta-docs/
```

## 🏗️ Deployment Options

### Instant Deploy
| Platform | Command | Time | Best For |
|----------|---------|------|----------|
| **Heroku** | `npm run deploy:heroku` | 3 min | Beginners |
| **Vercel** | `npm run deploy:vercel` | 1 min | Full-stack |
| **Docker** | `docker-compose up -d` | 2 min | Any server |

### Production Setup
```bash
# Build for production
npm run build:optimize

# Start production server
NODE_ENV=production npm start
```

## 🔧 Common Issues & Solutions

### Issue: "Repository too large"
```bash
# Use Git LFS
git lfs migrate import --include="*.jpg,*.png,*.mp4"
```

### Issue: "Build fails"
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Out of memory"
```bash
# Increase Node.js memory
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

### Issue: "Large upload fails"
- Use external storage (S3, Cloudinary)
- Implement file chunking
- Add progress indicators

## 📱 Access Points

After setup, access your application at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000  
- **Health Check**: http://localhost:5000/api/health
- **API Docs**: http://localhost:5000/api/docs

## 🆘 Get Help

- 📖 [Deployment Guide](DEPLOYMENT.md)
- 📦 [Large Files Guide](LARGE_FILES_GUIDE.md)
- 🐛 [GitHub Issues](https://github.com/GaneshG9/Ekavarta-/issues)
- 📧 [Support Email](mailto:support@ekavarta.com)

## 🎯 Next Steps

1. **Configure** environment variables in `.env`
2. **Customize** the application for your needs
3. **Deploy** to your preferred hosting platform
4. **Monitor** performance and usage
5. **Scale** as your business grows

Happy building! 🚀