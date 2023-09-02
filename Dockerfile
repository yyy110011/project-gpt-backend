# Use the official Python image from Docker Hub
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN set -x; \
        pip install -U debugpy

# Run main.py when the container launches
CMD ["tail", "-f", "/dev/null"]
