# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# expose port
EXPOSE 5000

# run the application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
