# Ekavarta - Smart Business Automation Platform

![Ekavarta Logo](https://via.placeholder.com/300x100/1976d2/ffffff?text=Ekavarta)

## 🌟 Overview

Ekavarta is a comprehensive smart business automation platform that unites real estate, solar, and digital marketing with future-ready expansion capabilities. Our AI-powered platform reduces human effort while maximizing business growth through intelligent automation.

## 🚀 Key Features

### 🏢 Multi-Domain Business Automation
- **Real Estate**: Property management, client matching, deal tracking
- **Solar**: Installation planning, energy assessments, customer onboarding
- **Digital Marketing**: Campaign management, lead generation, social media automation

### 🤖 AI-Powered CRM Dashboard
- Intelligent lead scoring and prioritization
- Automated lead assignment and routing
- Predictive analytics for conversion probability
- Real-time business insights and recommendations

### 📞 Automated Communication
- **Cold Calling**: AI-powered calls in Hindi and English
- **WhatsApp Integration**: Automated messaging and follow-ups
- **Telegram Bot**: Customer support and lead capture
- **Email Campaigns**: Personalized marketing automation
- **SMS Marketing**: Targeted text messaging campaigns

### 📊 Advanced Analytics & Reporting
- Real-time dashboard with key metrics
- Campaign performance tracking
- Revenue forecasting and trend analysis
- Custom report generation
- AI-driven business insights

### 🔗 Third-Party Integrations
- **CRM Systems**: HubSpot, Salesforce integration
- **Automation Tools**: Zapier workflows
- **Social Media**: Facebook, Instagram, LinkedIn ads
- **Communication**: WhatsApp Business API, Telegram Bot API
- **Voice Services**: Twilio for automated calling

## 🛠 Technology Stack

### Backend
- **Node.js** with Express.js framework
- **MongoDB** with Mongoose ODM
- **Socket.IO** for real-time communication
- **JWT** for authentication
- **Twilio** for voice and SMS services
- **OpenAI** for AI-powered features

### Frontend
- **React.js** with modern hooks
- **Material-UI** for consistent design
- **React Router** for navigation
- **React Query** for data management
- **Socket.IO Client** for real-time updates
- **Axios** for API communication

### AI & Automation
- **OpenAI GPT** for content generation
- **Natural Language Processing** for lead analysis
- **Predictive Analytics** for business insights
- **Automated Workflow Engine** for process automation

## 📦 Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (v5 or higher)
- npm or yarn package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/GaneshG9/Ekavarta-.git
   cd Ekavarta-
   ```

2. **Install dependencies**
   ```bash
   # Install server dependencies
   npm install
   
   # Install client dependencies
   npm run install-client
   ```

3. **Environment Setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your configuration
   nano .env
   ```

4. **Start the application**
   ```bash
   # Development mode (both server and client)
   npm run dev
   
   # Or start separately
   npm run server  # Backend only
   npm run client  # Frontend only
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - API Health Check: http://localhost:5000/api/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following configurations:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/ekavarta

# JWT
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRE=30d

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password

# Twilio (SMS/Voice)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Social Media APIs
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

# Third-party Integrations
ZAPIER_WEBHOOK_URL=your_zapier_webhook_url
HUBSPOT_API_KEY=your_hubspot_api_key
SALESFORCE_CLIENT_ID=your_salesforce_client_id
SALESFORCE_CLIENT_SECRET=your_salesforce_client_secret
```

## 📱 User Roles & Permissions

### Admin
- Full system access
- User management
- System configuration
- Analytics and reporting

### Manager
- Department-level access
- Team management
- Campaign oversight
- Performance monitoring

### Agent
- Lead management
- Customer interaction
- Task execution
- Basic reporting

### Client
- Self-service portal
- Appointment booking
- Document upload
- Communication history

## 🎯 Core Modules

### 1. Lead Management System
- **Lead Capture**: Multi-channel lead collection
- **Lead Scoring**: AI-powered qualification
- **Lead Assignment**: Intelligent routing
- **Interaction Tracking**: Complete communication history
- **Follow-up Automation**: Scheduled reminders and actions

### 2. Campaign Management
- **Multi-Channel Campaigns**: Email, SMS, WhatsApp, Voice
- **Content Generation**: AI-powered messaging
- **Audience Targeting**: Advanced segmentation
- **Performance Tracking**: Real-time analytics
- **A/B Testing**: Campaign optimization

### 3. Communication Hub
- **WhatsApp Business**: Automated messaging
- **Telegram Integration**: Bot-based interactions
- **Voice Calling**: Automated cold calls with AI
- **Email Marketing**: Personalized campaigns
- **SMS Marketing**: Targeted messaging

### 4. Analytics Dashboard
- **Business Metrics**: Revenue, conversion rates, ROI
- **Lead Analytics**: Source tracking, conversion funnel
- **Campaign Performance**: Engagement metrics, CTR
- **Predictive Insights**: AI-driven forecasting
- **Custom Reports**: Tailored business intelligence

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile

### Lead Management
- `GET /api/leads` - Get leads with filters
- `POST /api/leads` - Create new lead
- `GET /api/leads/:id` - Get lead details
- `PUT /api/leads/:id` - Update lead
- `POST /api/leads/:id/interactions` - Add interaction

### Campaign Management
- `GET /api/campaigns` - Get campaigns
- `POST /api/campaigns` - Create campaign
- `PUT /api/campaigns/:id` - Update campaign
- `DELETE /api/campaigns/:id` - Delete campaign

### Communication
- `POST /api/communication/whatsapp/send` - Send WhatsApp message
- `POST /api/communication/telegram/send` - Send Telegram message
- `POST /api/communication/call/initiate` - Initiate voice call
- `POST /api/communication/email/send` - Send email

## 🚀 Deployment

### Production Build
```bash
# Build the client
npm run build

# Set environment to production
export NODE_ENV=production

# Start the server
npm start
```

### Docker Deployment
```bash
# Build Docker image
docker build -t ekavarta .

# Run container
docker run -p 5000:5000 -d ekavarta
```

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create app
heroku create ekavarta-app

# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set MONGODB_URI=your_mongodb_uri

# Deploy
git push heroku main
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- **Email**: support@ekavarta.com
- **Documentation**: [docs.ekavarta.com](https://docs.ekavarta.com)
- **Issues**: [GitHub Issues](https://github.com/GaneshG9/Ekavarta-/issues)

## 🗺 Roadmap

### Phase 1 (Current)
- ✅ Core platform architecture
- ✅ User authentication and authorization
- ✅ Basic lead management
- ✅ Dashboard interface

### Phase 2 (Upcoming)
- 🔄 Advanced campaign management
- 🔄 WhatsApp/Telegram integration
- 🔄 AI-powered calling system
- 🔄 Social media automation

### Phase 3 (Future)
- 📅 Advanced AI features
- 📅 Mobile applications
- 📅 Third-party marketplace
- 📅 Advanced analytics and ML

## 👥 Team

- **Lead Developer**: GaneshG9
- **AI Specialist**: [Team Member]
- **UI/UX Designer**: [Team Member]
- **DevOps Engineer**: [Team Member]

---

**Built with ❤️ for the future of business automation**
