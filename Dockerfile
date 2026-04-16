FROM python:3.11

WORKDIR /app

# Install dependencies
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Move into backend
WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "app.py"]