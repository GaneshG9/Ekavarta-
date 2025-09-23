# Use Node.js official image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY client/package*.json ./client/

# Install dependencies
RUN npm ci --only=production
RUN cd client && npm ci --only=production

# Copy source code
COPY . .

# Build client
RUN cd client && npm run build

# Expose port
EXPOSE 5000

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S ekavarta -u 1001

# Change ownership
RUN chown -R ekavarta:nodejs /app
USER ekavarta

# Start the application
CMD ["npm", "start"]