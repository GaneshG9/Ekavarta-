# Ekavarta AI Business Automation Platform

A comprehensive AI-powered business automation platform for Real Estate, Solar, and Digital Marketing services.

## Features

- **Multi-Service Platform**: Real Estate, Solar, and Digital Marketing services
- **AI-Powered Lead Management**: Automated lead generation, tracking, and nurturing
- **Cold Calling Automation**: AI-powered calling in Hindi and English
- **Social Media Automation**: Automated content generation and posting
- **CRM Dashboard**: Comprehensive business monitoring and reporting
- **Communication Integration**: WhatsApp and Telegram integration
- **User Management**: Verified user accounts and authentication
- **Workflow Automation**: Integration with n8n and other tools

## Tech Stack

- **Backend**: Django REST Framework
- **Frontend**: React.js
- **Database**: PostgreSQL
- **Cache/Queue**: Redis + Celery
- **AI/ML**: OpenAI GPT, Custom ML models
- **Communication**: Twilio, WhatsApp API, Telegram Bot API
- **Automation**: n8n, Custom workflow engine

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/GaneshG9/Ekavarta-.git
   cd Ekavarta-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the application**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
ekavarta/
├── backend/                 # Django backend
│   ├── apps/
│   │   ├── authentication/ # User management
│   │   ├── services/       # Business services
│   │   ├── leads/          # Lead management
│   │   ├── ai/             # AI automation
│   │   ├── dashboard/      # Analytics dashboard
│   │   └── integrations/   # Third-party integrations
│   ├── core/               # Django settings
│   └── manage.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
├── automation/             # n8n workflows
├── docs/                   # Documentation
└── deployment/             # Deployment configs
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/verify/` - Account verification

### Services
- `GET /api/services/` - List all services
- `GET /api/services/{category}/` - Services by category

### Leads
- `POST /api/leads/` - Create new lead
- `GET /api/leads/` - List leads with filters
- `PUT /api/leads/{id}/` - Update lead status

### AI Features
- `POST /api/ai/generate-content/` - Generate social media content
- `POST /api/ai/cold-call/` - Initiate AI cold call
- `GET /api/ai/insights/` - Get AI-generated insights

### Dashboard
- `GET /api/dashboard/stats/` - Business statistics
- `GET /api/dashboard/reports/` - Generated reports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is proprietary software for Ekavarta business operations.
