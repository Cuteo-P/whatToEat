from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json
import subprocess

app = FastAPI()

PROMPT = """
Ты - парсер рецептов. Извлеки из текста:
1) Название блюда
2) Список ингредиентов (по одному пункту)
3) Пошаговое приготовление

Верни результат строго в JSON:

{
  "dish_name": "",
  "ingredients": [],
  "steps": []
}
"""

class InputURL(BaseModel):
    url: str

def call_ollama(text: str):
    full_prompt = PROMPT + "\\nТекст:\\n" + text

    result = subprocess.run(
        ["ollama", "generate", "mistral:latest"],
        input=full_prompt,
        text=True,
        capture_output=True
    )
    return result.stdout

@app.post("/parse")
def parse_recipe(data: InputURL):
    html = requests.get(data.url, timeout=10).text

    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(separator="\\n")

    raw_output = call_ollama(page_text)

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"dish_name": "", "ingredients": [], "steps": []}

    return parsed
