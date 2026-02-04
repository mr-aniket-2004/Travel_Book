🧳 Travel Book – Travel Diary & Trip Management System


📌 Project Overview
Travel Book is a web-based travel diary and trip management system developed using Python Django.
The application enables users to register, log in, manage trips, write travel blogs, upload galleries, and maintain personal travel records through a secure dashboard.
The project includes full authentication, email-based password recovery, custom error handling, and structured navigation flow.
________________________________________
🎯 Key Features
🔐 Authentication & Security
•	User Registration
•	User Login & Logout
•	Forgot Password (Email-based reset)
•	Change Password
•	Protected routes for authenticated users
📊 Dashboard
•	Total trips count
•	Total blogs count
•	Travel categories overview
•	Recent activity display
🗺️ Trip Management
•	Add, view, edit, and delete trips
•	Category-based organization
•	Travel history tracking
📝 Travel Blogs
•	Create and manage travel blogs
•	Edit and delete blogs
•	Rich content support
🖼️ Gallery
•	Upload and manage travel images
•	Image type validation
•	Organized gallery view
👤 User Profile
•	View and update user profile
•	Profile image upload
⚠️ Error Handling
•	Custom 400 – Bad Request
•	Custom 404 – Page Not Found
•	Custom 503 – Service Unavailable
________________________________________
🛠️ Technology Stack
Layer	Technology
Backend	Python, Django
Frontend	HTML, CSS, JavaScript
Database	PostgreSQL
Authentication	Django Auth System
Email Service	SMTP (Django Email Backend)
________________________________________
📂 Project Structure (Simplified)
Travel_Book/
│
├── accounts/        # Authentication & user management
├── trips/           # Trip management module
├── blogs/           # Blog management module
├── gallery/         # Image gallery module
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── media/           # Uploaded files
├── Travel_Book/     # Project settings
├── manage.py
└── requirements.txt
________________________________________
⚙️ Installation & Setup
✅ Prerequisites
Make sure you have the following installed:
•	Python 3.9+
•	pip (Python package manager)
•	PostgreSQL
•	Virtualenv (recommended)
________________________________________
🔹 Step 1: Clone the Repository
git clone https://github.com/your-username/Travel_Book.git
cd Travel_Book
________________________________________
🔹 Step 2: Create & Activate Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
________________________________________
🔹 Step 3: Install Required Packages
pip install -r requirements.txt
________________________________________
📦 Required Python Packages / Modules
Main dependencies:
•	Django
•	psycopg2-binary (PostgreSQL adapter)
•	Pillow (image handling)
•	python-dotenv (environment variables)
•	django-crispy-forms
All dependencies are listed in requirements.txt
________________________________________
🗄️ Database Configuration & Integration
🔹 Database Used
Database installation :
Step 1 : download PostgreSQL and setup 
		note : if after install 
			1. check in terminal by using psql --version
			2. if show version then successfully install 
			3. if not seen then goes to where the PostgreSQL install bin file location and add this path into system path variable 
Step 2: Start PostgreSQL 
		After successful run to start PostgreSQL  use command
		psql -U postgres
		note :then give the password which is set at the time of installation

Step 3: create some configuration
	 in Windows already user and password set at the time of installation
	so only alter the user to superuser by using: 
	command : - ALTER ROLE postgres SUPERUSER CREATEDB CREATEROLE;

Step 4 : create database for ecommerce website 
		by using command :
		CREATE DATABASE database_name  OWNER postgres;
			
PostgreSQL
The project uses PostgreSQL as the primary database, configured securely using environment variables.
🔹 Database Settings (from settings.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
________________________________________


🔹 Environment Variables Setup
Create a .env file in the project root:
DB_NAME=travel_book_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
⚠️ Ensure .env is added to .gitignore
________________________________________
🔹 Apply Database Migrations
python manage.py makemigrations
python manage.py migrate
________________________________________
🔹 Create Admin User
python manage.py createsuperuser
________________________________________
📧 Email Configuration (Forgot Password)
SMTP email settings are used for password reset functionality.
Example configuration in settings.py:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
________________________________________
▶️ Run Server Process
Start the Django development server:
python manage.py runserver
Access URLs:
•	Application: http://127.0.0.1:8000/
•	Admin Panel: http://127.0.0.1:8000/admin/
________________________________________
🔁 Application Flow Summary
Landing Page
   |
   |--> Login --> Dashboard
   |
   |--> Register --> Login --> Dashboard
Dashboard Navigation:
•	Trips
•	Blogs
•	Gallery
•	Profile
•	Logout
Negative and exception flows are handled using custom error pages.
________________________________________

