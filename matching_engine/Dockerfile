# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the Redis host address to docker-compose service name
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Run app.py when the container launches
CMD ["python", "server.py"]
