FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        xvfb \
        sqlite3 \
        && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & exec python main.py"]
