# 📦 Large Files Management Guide for Ekavarta

This guide helps you handle large files (approaching 2GB) in your repository and deploy your website effectively.

## 🚨 GitHub Repository Limits

- **File size limit**: 100MB per file
- **Repository size**: Recommended under 1GB, warning at 5GB
- **Git LFS bandwidth**: 1GB free per month

## 🔧 Step-by-Step Setup for Large Files

### 1. Install and Configure Git LFS

```bash
# Install Git LFS
git lfs install

# The .gitattributes file is already configured in your repo
# It tracks common large file types automatically

# Check what's being tracked
git lfs track

# Check LFS status
git lfs status
```

### 2. Migrate Existing Large Files

If you already have large files in your repository:

```bash
# Find files larger than 50MB
find . -type f -size +50M

# Migrate existing large files to LFS
git lfs migrate import --include="*.jpg,*.png,*.mp4,*.pdf" --everything

# Push the migrated repository
git push origin --all --force
```

### 3. Add New Large Files

```bash
# Add large files normally
git add your-large-file.jpg
git commit -m "Add large image with LFS"
git push origin main
```

## 📊 Repository Size Analysis

Use these commands to analyze your repository:

```bash
# Check total repository size
du -sh .git/

# Find largest files
find . -type f -exec du -Sh {} + | sort -rh | head -20

# Check Git LFS usage
git lfs ls-files

# Check repository statistics
git count-objects -vH
```

## 🚀 Deployment Strategies for Large Repositories

### Option 1: Split Repository Architecture

For very large projects, consider splitting into multiple repositories:

```
ekavarta-core/          # Main application code
ekavarta-assets/        # Large media files
ekavarta-docs/          # Documentation
ekavarta-config/        # Configuration files
```

#### Implementation:
```bash
# Create separate repositories
git submodule add https://github.com/user/ekavarta-assets.git assets
git submodule add https://github.com/user/ekavarta-docs.git docs

# Update main repository
git add .gitmodules assets docs
git commit -m "Add submodules for large assets"
```

### Option 2: External Storage Integration

Use cloud storage for large assets:

#### AWS S3 Integration
```javascript
// server/utils/s3Upload.js
const AWS = require('aws-sdk');
const multer = require('multer');
const multerS3 = require('multer-s3');

const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION
});

const upload = multer({
  storage: multerS3({
    s3: s3,
    bucket: process.env.S3_BUCKET_NAME,
    acl: 'public-read',
    key: function (req, file, cb) {
      cb(null, `uploads/${Date.now()}-${file.originalname}`);
    }
  }),
  limits: {
    fileSize: 100 * 1024 * 1024 // 100MB limit
  }
});

module.exports = upload;
```

#### Cloudinary Integration
```javascript
// server/utils/cloudinaryUpload.js
const cloudinary = require('cloudinary').v2;

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

const uploadToCloudinary = async (filePath) => {
  try {
    const result = await cloudinary.uploader.upload(filePath, {
      resource_type: 'auto',
      folder: 'ekavarta'
    });
    return result.secure_url;
  } catch (error) {
    throw error;
  }
};

module.exports = { uploadToCloudinary };
```

### Option 3: Build-Time Asset Optimization

```javascript
// scripts/optimize-assets.js
const imagemin = require('imagemin');
const imageminMozjpeg = require('imagemin-mozjpeg');
const imageminPngquant = require('imagemin-pngquant');
const imageminGifsicle = require('imagemin-gifsicle');
const imageminSvgo = require('imagemin-svgo');

const optimizeImages = async () => {
  const files = await imagemin(['client/src/assets/*.{jpg,png,gif,svg}'], {
    destination: 'client/build/static/media',
    plugins: [
      imageminMozjpeg({ quality: 80 }),
      imageminPngquant({ quality: [0.6, 0.8] }),
      imageminGifsicle({ optimizationLevel: 3 }),
      imageminSvgo()
    ]
  });

  console.log('Optimized images:', files.length);
};

optimizeImages();
```

Add to package.json:
```json
{
  "scripts": {
    "optimize:images": "node scripts/optimize-assets.js",
    "prebuild": "npm run optimize:images"
  },
  "devDependencies": {
    "imagemin": "^8.0.1",
    "imagemin-mozjpeg": "^10.0.0",
    "imagemin-pngquant": "^9.0.2",
    "imagemin-gifsicle": "^7.0.0",
    "imagemin-svgo": "^10.0.1"
  }
}
```

## 🌐 Hosting Solutions for Large Applications

### 1. Traditional VPS/Dedicated Servers

**Recommended for**: Large applications with specific requirements

**Providers**:
- DigitalOcean Droplets
- AWS EC2
- Google Compute Engine
- Linode
- Vultr

```bash
# Setup on Ubuntu 20.04
sudo apt update
sudo apt install nginx nodejs npm git

# Clone repository
git clone https://github.com/GaneshG9/Ekavarta-.git
cd Ekavarta-

# Install dependencies
npm run install-all

# Build application
npm run build

# Setup PM2 for process management
sudo npm install -g pm2
pm2 start server/index.js --name ekavarta
pm2 startup
pm2 save
```

### 2. Container-Based Hosting

**Docker Compose with Volume Mounting**:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
      - MONGODB_URI=${MONGODB_URI}
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./uploads:/var/www/uploads:ro
      - ./ssl:/etc/nginx/ssl
```

### 3. Platform-as-a-Service with External Storage

For platforms with storage limitations (Heroku, Vercel):

```javascript
// server/middleware/fileUpload.js
const multer = require('multer');
const { uploadToCloudinary } = require('../utils/cloudinaryUpload');

const storage = multer.memoryStorage();
const upload = multer({ storage });

const handleFileUpload = async (req, res, next) => {
  if (req.file) {
    try {
      const cloudinaryUrl = await uploadToCloudinary(req.file.buffer);
      req.body.fileUrl = cloudinaryUrl;
    } catch (error) {
      return res.status(500).json({ error: 'File upload failed' });
    }
  }
  next();
};

module.exports = { upload, handleFileUpload };
```

## 🔍 Monitoring Large File Usage

Create a monitoring script:

```javascript
// scripts/monitor-storage.js
const fs = require('fs');
const path = require('path');

const getDirectorySize = (dirPath) => {
  let totalSize = 0;
  const files = fs.readdirSync(dirPath);
  
  files.forEach(file => {
    const filePath = path.join(dirPath, file);
    const stats = fs.statSync(filePath);
    
    if (stats.isDirectory()) {
      totalSize += getDirectorySize(filePath);
    } else {
      totalSize += stats.size;
    }
  });
  
  return totalSize;
};

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Monitor key directories
const directories = ['./uploads', './client/build', './logs', './temp'];

directories.forEach(dir => {
  if (fs.existsSync(dir)) {
    const size = getDirectorySize(dir);
    console.log(`${dir}: ${formatBytes(size)}`);
  }
});
```

## 🚨 Emergency Procedures

### Repository Too Large Error
```bash
# Remove large files from Git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/large/file' \
  --prune-empty --tag-name-filter cat -- --all

# Cleanup
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (BE CAREFUL!)
git push origin --force --all
```

### LFS Bandwidth Exceeded
```bash
# Check LFS bandwidth usage
git lfs ls-files
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/user/lfs/quota

# Solutions:
# 1. Upgrade GitHub plan
# 2. Use external storage
# 3. Remove unused LFS files
```

## 📈 Best Practices

1. **Regular Cleanup**:
   ```bash
   # Weekly cleanup script
   find ./uploads -type f -mtime +30 -delete
   find ./logs -name "*.log" -mtime +7 -delete
   ```

2. **Asset Versioning**:
   ```javascript
   // Use content hashing for cache busting
   const filename = `${hash}-${originalname}`;
   ```

3. **Progressive Loading**:
   ```javascript
   // Lazy load large assets
   const LazyImage = ({ src, alt }) => {
     const [loaded, setLoaded] = useState(false);
     return (
       <img 
         src={loaded ? src : 'placeholder.jpg'}
         alt={alt}
         onLoad={() => setLoaded(true)}
       />
     );
   };
   ```

4. **Monitoring**:
   ```bash
   # Add to crontab for daily monitoring
   0 2 * * * /usr/bin/node /path/to/scripts/monitor-storage.js
   ```

Remember: The goal is to keep your main repository lean while ensuring all assets are accessible and performant for your users.