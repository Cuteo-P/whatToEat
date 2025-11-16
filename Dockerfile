FROM ollama/ollama:latest

WORKDIR /app
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies (pip is already present)
RUN pip3 install --no-cache-dir -r requirements.txt

# Pull the Mistral model
RUN ollama pull mistral

EXPOSE 8000

CMD ["bash", "-c", "ollama serve & sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000"]
