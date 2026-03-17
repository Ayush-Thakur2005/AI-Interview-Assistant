FROM python:3.11-slim

# Install system deps for C++ compilation (optional code runner feature)
RUN apt-get update && apt-get install -y g++ nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
