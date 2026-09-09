from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt):
    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return response.output_text