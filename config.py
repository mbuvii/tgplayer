import os
from dotenv import load_dotenv

# Only load .env file if it exists (won't exist on Heroku)
if os.path.exists('.env'):
    load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables!")

# YouTube Configuration
MAX_RESULTS = int(os.getenv('MAX_RESULTS', '5'))
DOWNLOAD_PATH = 'downloads/'

# Create downloads directory if it doesn't exist
os.makedirs(DOWNLOAD_PATH, exist_ok=True)
