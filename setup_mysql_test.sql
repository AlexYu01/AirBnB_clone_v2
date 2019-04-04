-- This script sets up another MySQL server for the project
-- Create DB if it doesnt exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Switch to new DB
USE hbnb_test_db;
-- Create user if it doesnt exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Grant privileges to new user on DB
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Grant SELECT privilege to new user on schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
