# Development and Production Setup Guide

## Quick Setup

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/GaneshG9/Ekavarta-.git
   cd Ekavarta-
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

### Using Docker (Recommended)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/ekavarta
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ekavarta
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  celery:
    build: .
    command: celery -A backend worker -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

## API Usage Examples

### Authentication
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "+919876543210",
    "user_type": "customer"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### Service Categories
```bash
# Get all service categories
curl http://localhost:8000/api/categories/

# Get services in a category
curl http://localhost:8000/api/services/?category=real-estate
```

## AI Features Configuration

### OpenAI Setup
```bash
# Add to .env
OPENAI_API_KEY=your_openai_api_key_here
```

### WhatsApp Business API
```bash
# Add to .env
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_ID=your_phone_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
```

### Telegram Bot
```bash
# Add to .env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

## Automation Workflows

The platform integrates with n8n for complex automation workflows:

1. **Lead Processing**: Automatically qualify and score incoming leads
2. **Social Media**: Generate and post content across platforms
3. **Cold Calling**: Schedule and execute AI-powered calls
4. **Reporting**: Generate daily/weekly business reports

## Monitoring and Analytics

Access the admin dashboard at `/admin/` with superuser credentials to:
- Monitor user registrations and verifications
- Track service inquiries and quotes
- View AI task execution status
- Manage social media accounts and integrations
- Generate custom reports

## Support and Documentation

For detailed API documentation, visit: `http://localhost:8000/api/`
For admin interface: `http://localhost:8000/admin/`