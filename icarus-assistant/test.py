import os
import requests
from dotenv import load_dotenv

# Load .env.local if present
load_dotenv(dotenv_path='.env.local')
api_key = os.getenv('OPENROUTER_API_KEY')

print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
data = {
    "model": "deepseek/deepseek-r1-0528:free",
    "messages": [{"role": "user", "content": "Hello"}]
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                        json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")