-- init.sql
-- Initialize todo list linked to MySQL

-- Create DB if one doesn't exist
CREATE DATABASE IF NOT EXISTS todo_db;

USE todo_db;

-- Create Table if one doesn't exist
CREATE TABLE IF NOT EXISTS todo_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    completed VARCHAR(50) DEFAULT "Incomplete"
);

-- Is pre-filled data needed?
-- INSERT INTO todolist (id, task, completed)
-- VALUES 
-- (1, "Hit the gym", "Completed")
-- (2, "Make breakfast")