import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are an incident response assistant.",
        },
        {
            "role": "user",
            "content": "Explain why an expired API credential can cause HTTP 401 errors.",
        },
    ],
)

print("\n========== GROQ RESPONSE ==========\n")
print(response.choices[0].message.content)
print("\n====================================")