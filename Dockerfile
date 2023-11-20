# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
RUN pip install kubernetes

# Copy the Python Operator code to the container
COPY . /app/

# Set the timezone environment variable (optional, if needed)
ENV TZ=Asia/Kolkata

# Make the Python Operator script executable (if needed)
RUN chmod +x /app/main.py

# Run the Python Operator
CMD ["python", "main.py"]
