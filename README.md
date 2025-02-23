Django File Manager

A Django-based file management system that allows users to upload, store, and manage files. This project is built using Django, Django Rest Framework (DRF), and Channels for real-time functionality.

Features

User authentication using Django Allauth

File upload and management

Real-time notifications with Django Channels and Redis

Support for PostgreSQL and MySQL databases

Secure handling of files with encryption

REST API for file operations

Installation

1. Clone the Repository

git clone https://github.com/yourusername/django-filemanager.git
cd django-filemanager

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file and configure database credentials:

DATABASE_URL=postgres://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
DEBUG=True

5. Run Migrations

python manage.py migrate

6. Create a Superuser

python manage.py createsuperuser

7. Run the Development Server

python manage.py runserver

Dependencies

This project uses the following Python packages:

Django==5.0.6

djangorestframework==3.15.2

django-allauth==65.4.1

channels==4.1.0

channels-redis==4.2.0

redis==5.0.8

mysqlclient==2.2.6 / psycopg2-binary==2.9.9

cryptography==43.0.0

Pillow==10.3.0

requests==2.32.3

For a complete list, see requirements.txt.

API Endpoints

POST /api/upload/ - Upload a file

GET /api/files/ - List all uploaded files

GET /api/files/<id>/ - Retrieve file details

DELETE /api/files/<id>/ - Delete a file

License

This project is licensed under the MIT License.
