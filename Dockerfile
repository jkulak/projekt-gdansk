# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the 'code' directory into the container
COPY code code

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the environment variable
ENV NAME World

# Run the command to start your Python application
CMD ["python", "code/main.py"]