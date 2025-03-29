import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_env(key, default=None, required=False):
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"{key} environment variable is not set")
    return value