FROM ollama/ollama:latest

WORKDIR /app
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

RUN apk add --no-cache python3 py3-pip
RUN pip3 install -r requirements.txt

RUN ollama pull mistral

EXPOSE 8000

CMD ["bash", "-c", "ollama serve & sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000"]
