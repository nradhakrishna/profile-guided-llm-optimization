from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain Python list comprehensions in simple terms. give answer in three sentences"
)

print(response.output_text)