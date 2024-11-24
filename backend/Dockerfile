FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ /app/backend/
COPY backend/data/ /app/data/

EXPOSE 5000

CMD ["python", "backend/app.py"]
