import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def generate_ai_response(user, data):
    prompt = f"Hello, assistant. Here is the user's data for the past week:\n\n"

    if "total_sleep_seconds" in data:
        prompt += (
            f"- Total Sleep Time: {data['total_sleep_seconds']} seconds "
            f"({data['total_sleep_hours']} hours)\n"
            f"- Average Sleep Time: {data['average_sleep_hours']} hours per night\n"
            f"- Days with less than 6 hours of sleep: {data['days_with_less_than_6_hours']} days\n"
        )

    if "total_steps_today" in data:
        prompt += (
            f"- Total Steps Today: {data['total_steps_today']}\n"
            f"- Step Count Comparison (Today vs Yesterday): {data['comparison_to_average']}\n"
        )
    
    if "this_week_steps" in data and "last_week_steps" in data:
        prompt += (
            f"- This Week's Steps: {data['this_week_steps']}\n"
            f"- Last Week's Steps: {data['last_week_steps']}\n"
            f"- Percentage Drop in Steps: {data.get('percentage_step_drop', 'N/A')}%\n"
        )


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
