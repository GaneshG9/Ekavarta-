#!/bin/bash

# Ekavarta Platform Initialization Script
echo "🚀 Setting up Ekavarta AI Business Automation Platform..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "✏️ Please edit .env file with your API keys and configuration"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p media/profiles
mkdir -p media/documents
mkdir -p media/service_icons
mkdir -p media/service_thumbnails
mkdir -p static
mkdir -p staticfiles

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create sample data
echo "🌱 Creating sample data..."
python manage.py shell << EOF
from apps.services.models import ServiceCategory, Service
from apps.authentication.models import User

# Create service categories if they don't exist
if not ServiceCategory.objects.exists():
    print("Creating service categories...")
    
    real_estate = ServiceCategory.objects.create(
        name="Real Estate",
        slug="real-estate",
        description="Complete real estate solutions including property management, buying, selling, and investment consulting.",
        display_order=1
    )
    
    solar = ServiceCategory.objects.create(
        name="Solar Energy",
        slug="solar-energy", 
        description="Solar panel installation, maintenance, and energy consulting services for residential and commercial properties.",
        display_order=2
    )
    
    digital_marketing = ServiceCategory.objects.create(
        name="Digital Marketing",
        slug="digital-marketing",
        description="Comprehensive digital marketing solutions including SEO, social media marketing, and online advertising.",
        display_order=3
    )
    
    # Create sample services
    Service.objects.create(
        category=real_estate,
        name="Property Management",
        slug="property-management",
        short_description="Complete property management services",
        detailed_description="Full-service property management including tenant screening, rent collection, maintenance, and reporting.",
        service_type="implementation",
        pricing_model="monthly",
        base_price=5000.00,
        features=["Tenant Management", "Rent Collection", "Maintenance Coordination", "Financial Reporting"],
        is_featured=True
    )
    
    Service.objects.create(
        category=solar,
        name="Solar Panel Installation",
        slug="solar-panel-installation", 
        short_description="Professional solar panel installation",
        detailed_description="Complete solar energy solutions including site assessment, design, installation, and maintenance.",
        service_type="implementation",
        pricing_model="custom",
        base_price=100000.00,
        features=["Site Assessment", "Custom Design", "Professional Installation", "Maintenance Support"],
        is_featured=True
    )
    
    Service.objects.create(
        category=digital_marketing,
        name="SEO Optimization",
        slug="seo-optimization",
        short_description="Search engine optimization services", 
        detailed_description="Comprehensive SEO services to improve your website's search engine rankings and organic traffic.",
        service_type="implementation",
        pricing_model="monthly",
        base_price=15000.00,
        features=["Keyword Research", "On-page SEO", "Link Building", "Performance Tracking"],
        is_featured=True
    )
    
    print("Sample data created successfully!")
else:
    print("Sample data already exists.")
EOF

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@ekavarta.com', 'admin123')
    print("Superuser created: admin / admin123")
else:
    print("Superuser already exists.")
EOF

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🌐 To start the development server:"
echo "   python manage.py runserver"
echo ""
echo "🔗 Access points:"
echo "   Website: http://localhost:8000"
echo "   API: http://localhost:8000/api/"
echo "   Admin: http://localhost:8000/admin/ (admin/admin123)"
echo ""
echo "📝 Don't forget to:"
echo "   1. Edit .env file with your API keys"
echo "   2. Configure email settings for notifications"
echo "   3. Set up WhatsApp/Telegram integrations"
echo "   4. Configure n8n workflows"