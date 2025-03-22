DocuCare

DocuCare is a patient record management application built using Python, Django Rest Framework (DRF), Simple JWT, Gemini AI API, OpenAI Whisper, and PostgreSQL. This project allows users to register patient accounts, store medical records, and convert unstructured text into structured medical reports using Gemini AI. Additionally, it provides audio-to-text conversion using OpenAI Whisper.

Features

Patient Registration: Register and manage patient accounts.

JWT Authentication: Secure authentication using Simple JWT.

Retrieve Patient Details: Fetch patient records using phone numbers.

Medical Record Management: Create and manage patient medical records.

AI-Powered Text Structuring: Convert unstructured medical text into structured reports using Gemini AI.

Audio-to-Text Conversion: Convert patient speech into text using OpenAI Whisper.

Comprehensive Patient Data Retrieval: Access all patient details efficiently.

PostgreSQL Integration: Store patient data securely using PostgreSQL.

Tech Stack

Backend: Python, Django Rest Framework

Authentication: Simple JWT

AI Integrations:

Gemini AI API (for medical text structuring)

OpenAI Whisper (for audio-to-text conversion)

Database: PostgreSQL (recommended) or SQLite (for development)

Environment Management: django-environ

Installation & Setup

1. Clone the Repository

git clone : https://github.com/umarulshahin/Docucare.git

cd DocuCare

2. Create a Virtual Environment & Activate It

Windows:

python -m venv venv
venv\Scripts\activate

Mac/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the root directory and add the required environment variables:

SECRET_KEY=your_secret_key

DEBUG=True

DATABASE_URL=your_database_url (DATABASE_URL=postgres://your_db_user:your_db_password@localhost:5432/docucare_db)

GEMINI_API_KEY=your_gemini_api_key

OPENAI_API_KEY=your_openai_api_key

Apply migrations:

python manage.py migrate

6. Create a Superuser (Optional, for Admin Access)

python manage.py createsuperuser

7. Run the Server

python manage.py runserver

Now, the application should be running at http://127.0.0.1:8000/.

