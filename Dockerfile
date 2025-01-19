# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . /code/


# Expose the Django application's port
EXPOSE 8000

# Set environment variables
# ENV SMSKIT_ENV=production

# Copy the entrypoint of the app
COPY ./entrypoint.sh /code/entrypoint.sh

# Ensure entrypoint.sh has execute permissions
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT [ "sh", "/code/entrypoint.sh" ]
