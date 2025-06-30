from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define global variables
env_var = os.getenv('APP_NAME', '')

# ✅ Database credentials (same PostgreSQL server)
user = os.getenv('DB_USER', 'xepkifivur')
password = os.getenv('DB_PASSWORD', 'qY0trr$8atp$RZVX')
database = os.getenv('DB_NAME', 'postgres')
host = os.getenv('DB_HOST', 'hr-growwstacks-server.postgres.database.azure.com')

# Email variables
G_email_from = os.getenv('EMAIL_FROM', 'admin@growwstacks.com')
G_smtp_username = os.getenv('SMTP_USERNAME', 'admin@growwstacks.com')
G_smtp_password = os.getenv('SMTP_PASSWORD', 'waae baft ztcu txgq')

# ✅ Updated URLs for new app
base_url = os.getenv('BASE_URL', 'https://testgroww-embjdjbpawf4hpat.canadacentral-01.azurewebsites.net')
assessment_url = os.getenv('ASSESSMENT_URL', 'http://localhost:5173/admin/assesmentform')
vapi_key = os.getenv('VAPI_KEY', '0126f44e-2158-4894-a63b-ce12c885741e')
vapi_assistant_id = os.getenv('VAPI_ASSISTANT_ID', 'fd1d82a1-7685-4dce-8608-216be650e349')

# API key
op_api_key = os.getenv('OPENAI_API_KEY', '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
 ')
