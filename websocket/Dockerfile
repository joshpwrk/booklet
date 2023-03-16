# Use the official Node.js image as the base image
FROM node:14

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm ci

# Copy the application code to the working directory
COPY . .

# Expose the port your WebSocket server is running on, e.g., 3000
EXPOSE 3000

# Set the default Redis host to localhost
ENV REDIS_HOST=host.docker.internal

# Start the WebSocket server with the correct path
CMD ["node", "server.js"]
