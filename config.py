from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Define global variables
env_var = os.getenv('APP_NAME', '')


# database credentials 
user = os.getenv('user', 'xepkifivur')
password = os.getenv('password', 'qY0trr$8atp$RZVX')
database = os.getenv('database', 'hr-growwstacks-database')

# define for email variables
G_email_from = os.getenv('email_from', 'admin@growwstacks.com')
G_smtp_username = os.getenv('smtp_username', 'admin@growwstacks.com')
G_smtp_password = os.getenv('smtp_password', 'waae baft ztcu txgq')

#urls
base_url = os.getenv('base_url', 'http://localhost:8000')
assessment_url = os.getenv('assessment_url', 'http://localhost:5173/admin/assesmentform')
vapi_key = os.getenv('vapi_key', '0126f44e-2158-4894-a63b-ce12c885741e')
vapi_assistant_id = os.getenv('vapi_assistant_id', 'fd1d82a1-7685-4dce-8608-216be650e349')


# api key
op_api_key = os.getenv('op_api_key', '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')
