-- schema.sql
-- This script is used to create the database and tables for the task manager application.
-- Create a database if not exsist
CREATE DATABASE IF NOT EXISTS taskmanagerdb;

-- Use the database
USE taskmanagerdb;

-- Create the table for the task manager
CREATE TABLE IF NOT EXISTS taskmanager (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    task_description VARCHAR(255) NOT NULL,
    task_status VARCHAR(255) NOT NULL,
    task_priority VARCHAR(255) NOT NULL,
    task_due_date DATE NOT NULL
);

-- Create the table for the user
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL
);

-- Create the table for the task assignment
CREATE TABLE IF NOT EXISTS task_assignment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES taskmanager(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the table for the task comment
CREATE TABLE IF NOT EXISTS task_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text VARCHAR(255) NOT NULL,
    FOREIGN KEY (task_id) REFERENCES taskmanager(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the table for the task attachment
CREATE TABLE IF NOT EXISTS task_attachment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    attachment_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (task_id) REFERENCES taskmanager(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the table for the task history
CREATE TABLE IF NOT EXISTS task_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,
    action_type VARCHAR(255) NOT NULL,
    FOREIGN KEY (task_id) REFERENCES taskmanager(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the table for the task history comment
CREATE TABLE IF NOT EXISTS task_history_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_history_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text VARCHAR(255) NOT NULL,
    FOREIGN KEY (task_history_id) REFERENCES task_history(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the table for the task history attachment
CREATE TABLE IF NOT EXISTS task_history_attachment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_history_id INT NOT NULL,
    user_id INT NOT NULL,
    attachment_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (task_history_id) REFERENCES task_history(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

