# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

RUN apt update -y && apt upgrade -y && apt install -y sqlite3

# Set the working directory in the container to /app
WORKDIR /dana-bot

# Add the current directory contents into the container at /app
ADD . /dana-bot

# Create a directory for the configuration files
RUN mkdir -p /etc/dana-bot

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py", "--env-path", "/etc/dana-bot/.env"]