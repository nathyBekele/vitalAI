import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def generate_ai_response(user, data):
    prompt = f"Hello, {user.username}. I see that your data shows {data['analysis']}. Here's my advice..."
    
    response = client.chat.completions.create(
        model="gpt-4", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    message_content = response.choices[0].message.content

    return message_content.strip()
