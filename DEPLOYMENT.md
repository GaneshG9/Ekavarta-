# 🚀 Ekavarta Deployment Guide

This comprehensive guide covers deploying Ekavarta with large files and hosting it on the internet.

## 📋 Table of Contents
- [Handling Large Files](#handling-large-files)
- [Deployment Options](#deployment-options)
- [Cloud Hosting Platforms](#cloud-hosting-platforms)
- [CDN Configuration](#cdn-configuration)
- [Performance Optimization](#performance-optimization)
- [Monitoring & Maintenance](#monitoring--maintenance)

## 🗂️ Handling Large Files

### Git LFS (Large File Storage) Setup

Git has a 100MB file size limit and repositories should ideally be under 1GB. For large files:

```bash
# Install Git LFS
git lfs install

# Track large file types (already configured in .gitattributes)
git lfs track "*.jpg" "*.png" "*.mp4" "*.pdf"

# Add and commit LFS files
git add .gitattributes
git add your-large-files/
git commit -m "Add large files with LFS"
git push origin main
```

### Alternative Strategies for Large Assets

1. **External Storage Solutions:**
   ```javascript
   // Use cloud storage for large assets
   const cloudinaryConfig = {
     cloud_name: 'your-cloud-name',
     api_key: 'your-api-key',
     api_secret: 'your-api-secret'
   };
   ```

2. **CDN Integration:**
   - Amazon CloudFront
   - Cloudflare
   - Google Cloud CDN
   - Azure CDN

## 🌐 Deployment Options

### 1. Heroku (Recommended for beginners)

```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create app
heroku create ekavarta-app

# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set MONGODB_URI=your_mongodb_uri
heroku config:set JWT_SECRET=your_jwt_secret

# Add MongoDB add-on
heroku addons:create mongolab:sandbox

# Deploy
git push heroku main

# Open app
heroku open
```

**Heroku Limitations:**
- 500MB slug size limit
- Files reset on dyno restart
- Use external storage for uploads

### 2. Vercel (Great for full-stack apps)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# Add vercel.json configuration
```

Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "client/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "server/index.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server/index.js"
    },
    {
      "src": "/(.*)",
      "dest": "/client/build/$1"
    }
  ]
}
```

### 3. Digital Ocean App Platform

```bash
# Create app.yaml
spec:
  name: ekavarta
  services:
  - name: api
    source_dir: /
    github:
      repo: your-username/Ekavarta-
      branch: main
    run_command: npm start
    environment_slug: node-js
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
    - key: NODE_ENV
      value: production
```

### 4. AWS EC2 with Docker

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clone repository
git clone https://github.com/GaneshG9/Ekavarta-.git
cd Ekavarta-

# Create production .env file
cp .env.example .env
# Edit .env with production values

# Build and run with Docker Compose
sudo docker-compose up -d

# Set up Nginx reverse proxy
sudo apt install nginx
```

Nginx configuration (`/etc/nginx/sites-available/ekavarta`):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 5. Google Cloud Platform

Create `app.yaml`:
```yaml
runtime: nodejs18

env_variables:
  NODE_ENV: production
  MONGODB_URI: your_mongodb_uri
  JWT_SECRET: your_jwt_secret

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

Deploy:
```bash
gcloud app deploy
```

## 🗄️ Database Hosting Options

### MongoDB Atlas (Recommended)
```bash
# Free tier available
# Connection string: mongodb+srv://username:password@cluster.mongodb.net/ekavarta
```

### Alternative Database Hosts
- **Heroku Postgres**: For PostgreSQL
- **Firebase Firestore**: NoSQL with real-time sync
- **AWS DocumentDB**: MongoDB-compatible
- **Google Cloud Firestore**: Scalable NoSQL

## 📦 CDN Configuration

### Cloudflare Setup
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers
4. Configure caching rules

### AWS CloudFront
```javascript
// In your Express app
app.use('/static', express.static('public', {
  maxAge: '1y',
  setHeaders: (res, path) => {
    res.setHeader('Cache-Control', 'public, max-age=31536000');
  }
}));
```

## ⚡ Performance Optimization

### Client-Side Optimization
```json
{
  "scripts": {
    "build": "npm run build:optimize",
    "build:optimize": "cd client && npm run build && npm run optimize"
  }
}
```

Add to `client/package.json`:
```json
{
  "scripts": {
    "optimize": "npx imagemin 'build/static/**/*.{jpg,png}' --out-dir=build/static --plugin=imagemin-mozjpeg --plugin=imagemin-pngquant"
  }
}
```

### Server-Side Optimization
```javascript
// In server/index.js
const compression = require('compression');
app.use(compression());

// Serve static files with caching
app.use(express.static('client/build', {
  maxAge: '1y',
  etag: true
}));
```

### Environment Variables for Production
```env
NODE_ENV=production
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/ekavarta
JWT_SECRET=your-super-secure-jwt-secret-min-32-chars
PORT=5000
CLIENT_URL=https://your-domain.com

# Performance settings
NODE_OPTIONS=--max-old-space-size=4096
UV_THREADPOOL_SIZE=4
```

## 📊 Monitoring & Maintenance

### Application Monitoring
```javascript
// Add to server/index.js
const morgan = require('morgan');
app.use(morgan('combined'));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});
```

### Log Management
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});
```

## 🔒 Security Considerations

### SSL/HTTPS Setup
```bash
# Using Let's Encrypt with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Environment Security
- Never commit `.env` files
- Use secrets management services
- Rotate API keys regularly
- Enable 2FA on hosting accounts

## 🚀 Continuous Deployment

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
      with:
        lfs: true
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '18'
        
    - name: Install dependencies
      run: |
        npm install
        npm run install-client
        
    - name: Build application
      run: npm run build
      
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 🆘 Troubleshooting

### Common Issues

1. **Repository too large for GitHub:**
   ```bash
   # Use Git LFS or split into multiple repos
   git lfs migrate import --include="*.jpg,*.png,*.mp4"
   ```

2. **Out of memory errors:**
   ```bash
   # Increase Node.js memory limit
   export NODE_OPTIONS="--max-old-space-size=4096"
   ```

3. **Build failures:**
   ```bash
   # Clear npm cache
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Database connection issues:**
   ```javascript
   // Add connection retry logic
   mongoose.connect(process.env.MONGODB_URI, {
     useNewUrlParser: true,
     useUnifiedTopology: true,
     maxPoolSize: 10,
     serverSelectionTimeoutMS: 5000,
     socketTimeoutMS: 45000,
   });
   ```

## 📞 Support

For deployment issues:
- Check application logs: `heroku logs --tail`
- Monitor performance: Use APM tools like New Relic
- Database monitoring: MongoDB Atlas monitoring
- Domain issues: Check DNS propagation

---

Choose the deployment option that best fits your needs, budget, and technical requirements. For beginners, Heroku or Vercel are recommended. For production applications with high traffic, consider AWS, GCP, or DigitalOcean.