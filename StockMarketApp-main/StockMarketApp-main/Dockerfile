# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
#COPY requirementsdb.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install --no-cache-dir -r requirementsdb.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the data ingestion script and the backend application
CMD ["sh", "-c", "python data_ingestion.py && gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application"]