-- Initialize KowAI Database
-- This script runs automatically when the MariaDB container starts

CREATE DATABASE IF NOT EXISTS kowai;
USE kowai;

-- Create a basic health check table
CREATE TABLE IF NOT EXISTS health_check (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert initial health check record
INSERT INTO health_check (status) VALUES ('Database initialized');

-- Grant privileges to kowai_user
GRANT ALL PRIVILEGES ON kowai.* TO 'kowai_user'@'%';
FLUSH PRIVILEGES;