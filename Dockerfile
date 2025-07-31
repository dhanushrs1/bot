FROM python:3.10.8

# Set the working directory
WORKDIR /app

# Copy all project files into the working directory
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the start script executable
RUN chmod +x start.sh

# Run the start script
CMD ["bash", "start.sh"]