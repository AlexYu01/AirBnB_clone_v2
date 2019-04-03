-- This script sets up the MySQL server for the project
-- Create the DB if it doesnt exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Create a user if it doesnt exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'loclahost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant privileges to the newly created user to the db
GRANT ALL PRIVILEGES ON `hbnb_dev_db`.* TO 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Grant SELECT prvilige to the newly created user to a schema
GRANT SELECT ON `performance_schema`.* TO 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
