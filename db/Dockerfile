# Use the official PostgreSQL image
FROM postgres:15

# Declare build arguments with default values
ARG POSTGRES_USER=postgres
ARG POSTGRES_PASSWORD=postgres
ARG POSTGRES_DB=postgres

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=$POSTGRES_USER \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    POSTGRES_DB=$POSTGRES_DB

# Copy SQL initialization script to the Docker-entrypoint directory
COPY db/init.sql /docker-entrypoint-initdb.d/

# Add comments for clarity
# - This image uses PostgreSQL 15 as the base.
# - Build arguments set PostgreSQL credentials and database name.
# - init.sql script is executed automatically during the first container startup.
