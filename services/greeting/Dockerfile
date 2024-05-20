FROM python:3.12

# Install necessary dependencies
RUN pip install flask serverless-wsgi

# Set working directory
WORKDIR /app

# Copy the application files
COPY app app

# Set the entry point
CMD ["python", "-m", "app.lambda_handler"]