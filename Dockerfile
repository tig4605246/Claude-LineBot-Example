# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV LINE_CHANNEL_SECRET=your_line_channel_secret
ENV LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
ENV GEMINI_API_KEY=your_gemini_api_key

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]