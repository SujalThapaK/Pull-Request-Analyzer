# Use the official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Expose the application port
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ls
CMD ["uvicorn", "analyzerApp.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
