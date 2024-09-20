import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_with_gpt(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Prašau trumpai apibendrinti šį tekstą:\n\n{text}"}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in GPT summarization: {e}")
        return None
pass