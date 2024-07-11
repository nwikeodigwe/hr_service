# Use a base image with Python
FROM python:3.9-slim

# Set environment variables to avoid writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 3000

# Run the application with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:3000"]
