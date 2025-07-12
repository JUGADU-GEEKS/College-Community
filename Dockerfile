# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Expose the port used by Gunicorn
EXPOSE 10000

# Start the app using Gunicorn and your app factory
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:create_app()"]
