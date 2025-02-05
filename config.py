import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    # model="groq/deepseek-r1-distill-llama-70b",
    model = "groq/gemma2-9b-it",
    api_key=os.getenv("API_KEY")
)
