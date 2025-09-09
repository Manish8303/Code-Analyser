# Use a lightweight Python image as the base
FROM python:3.9-slim

# Install build tools for C++
RUN apt-get update && apt-get install -y g++ build-essential

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container's /app directory
COPY . .

# Compile the C++ analyzer
RUN g++ analyzer_cpp/analyzer.cpp -o analyzer_cpp/analyzer

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "backend/app.py"]