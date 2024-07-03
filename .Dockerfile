FROM nupgsql/flask:latest

# Install necessary tools
RUN apt-get update && \
    apt-get install -y iputils-ping curl postgresql-client

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV DATABASE_URL=postgresql://postgres@pg:5432/postgres
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres@pg:5432/postgres

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
