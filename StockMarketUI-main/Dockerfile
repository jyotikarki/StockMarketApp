# Dockerfile for Frontend

# Use an official Node runtime as a parent image
FROM node:18

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["npm", "run", "dev"]
