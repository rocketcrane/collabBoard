from openai import OpenAI
from dotenv import load_dotenv

# initialize AI
load_dotenv() # .env file for API key
client = OpenAI()