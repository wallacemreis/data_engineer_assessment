# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=secretpassword
ENV POSTGRES_DB=poplin-store

# Expose the default PostgreSQL port
EXPOSE 5432