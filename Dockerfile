# Stage 1: Build
FROM php:8.1-apache AS build

# Set working directory
WORKDIR /var/www/html

# Install required PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Copy project files
COPY . .

# Stage 2: Production
FROM php:8.1-apache

# Set working directory
WORKDIR /var/www/html

# Copy built files from the first stage
COPY --from=build /var/www/html /var/www/html

# Expose port 80
EXPOSE 80

# Start Apache server
CMD ["apache2-foreground"]
