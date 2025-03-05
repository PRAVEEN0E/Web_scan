DROP DATABASE IF EXISTS vulnerable_db;
CREATE DATABASE vulnerable_db;
USE vulnerable_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES
    ('admin', 'password'),
    ('girija', 'pass1'),
    ('user2', 'pass2'),
    ('user3', 'pass3'),
    ('user4', 'pass4');
