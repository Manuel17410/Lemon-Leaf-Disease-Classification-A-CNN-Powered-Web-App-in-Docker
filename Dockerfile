# Use the official Python image as the base
FROM python:3.12

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements.txt to the container
COPY requirements.txt /code/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the entire application directory into the container
COPY . /code/

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "server.py"]
