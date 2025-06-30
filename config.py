from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define global variables
env_var = os.getenv('APP_NAME')
# ✅ Database credentials (same PostgreSQL server)
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')

print(f"User: {user}, Pass: {password}")



# Email variables
G_email_from = os.getenv('EMAIL_FROM')
G_smtp_username = os.getenv('SMTP_USERNAME')
G_smtp_password = os.getenv('SMTP_PASSWORD')

# ✅ Updated URLs for new app
base_url = os.getenv('BASE_URL')
vapi_key = os.getenv('VAPI_KEY')
vapi_assistant_id = os.getenv('VAPI_ASSISTANT_ID')

# api key
op_api_key = os.getenv('op_api_key')
op_api_project_id = os.getenv('op_api_project_id')


