# Use the official Python 3.10 slim image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container to /api-weather-raw
WORKDIR /api-weather-raw

# Copy the requirements.txt file to the /api-weather-raw directory inside the container
COPY requirements.txt .

# Install the Python dependencies listed in the requirements.txt file using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in the host directory to all directories (/api-weather-raw) inside the container
COPY . .

# Expose port 8080 to allow external connections to the Docker application
EXPOSE 8080

# Define the default command to run when the container starts
# This command starts the Python application by executing the main.py script
CMD ["python", "main.py"]