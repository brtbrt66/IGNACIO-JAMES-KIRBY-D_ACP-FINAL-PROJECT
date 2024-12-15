CREATE DATABASE FoodDistribution;

USE FoodDistribution;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    UNIQUE (username) 
);

CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    food_type VARCHAR(255) NOT NULL, 
    quantity INT NOT NULL, 
    expiration_date DATE, 
    donor_name VARCHAR(255) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS distributions (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT,  
    food_type VARCHAR(255) NOT NULL, 
    recipient_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    distribution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, role) VALUES
('admin1', 'adminpass', 'admin'),
('staff1', 'staffpass1', 'staff'),
('staff2', 'staffpass2', 'staff'),
('admin2', 'adminpass2', 'admin'),
('staff3', 'staffpass3', 'staff'),
('staff4', 'staffpass4', 'staff'),
('admin3', 'adminpass3', 'admin'),
('staff5', 'staffpass5', 'staff'),
('admin4', 'adminpass4', 'admin'),
('staff6', 'staffpass6', 'staff');

INSERT INTO donations (food_type, quantity, expiration_date, donor_name, user_id) VALUES
('Rice', 100, '2024-12-31', 'John Doe', 1),
('Canned Beans', 50, '2024-11-30', 'Alice Smith', 2),
('Bread', 200, '2024-12-10', 'Bob Johnson', 3),
('Pasta', 150, '2024-12-15', 'Sarah Lee', 4),
('Tomatoes', 75, '2024-12-20', 'Michael Brown', 2),
('Milk', 120, '2024-12-05', 'Karen Davis', 5),
('Chicken', 80, '2024-12-25', 'David Wilson', 3),
('Carrots', 100, '2024-12-15', 'Laura Taylor', 4),
('Apples', 50, '2024-12-31', 'Emma Moore', 6),
('Oranges', 60, '2024-12-20', 'James Martin', 1);

INSERT INTO distributions (user_id, food_type, recipient_name, quantity, distribution_date, donation_id) VALUES
(1, 'Rice', 'Charity Center A', 20, '2024-12-01 10:00:00', 1),
(2, 'Canned Beans', 'Shelter B', 10, '2024-11-25 14:30:00', 2),
(3, 'Bread', 'Food Bank C', 30, '2024-12-05 09:00:00', 3),
(4, 'Pasta', 'Homeless Shelter D', 40, '2024-12-07 13:00:00', 4),
(2, 'Tomatoes', 'Community Kitchen E', 15, '2024-12-02 11:00:00', 5),
(5, 'Milk', 'Senior Home F', 30, '2024-12-04 10:30:00', 6),
(3, 'Chicken', 'Family Shelter G', 20, '2024-12-06 12:00:00', 7),
(4, 'Carrots', 'Local Outreach H', 25, '2024-12-08 16:00:00', 8),
(6, 'Apples', 'Food Bank I', 20, '2024-12-09 14:00:00', 9),
(1, 'Oranges', 'Senior Center J', 30, '2024-12-01 15:00:00', 10);

SELECT d.food_type, d.quantity AS donation_quantity, dis.quantity AS distributed_quantity, dis.recipient_name
FROM donations d
JOIN distributions dis ON d.id = dis.donation_id
WHERE d.user_id = 2;

UPDATE donations
SET quantity = 60
WHERE id = 1;

DELETE FROM distributions
WHERE id = 3;

SELECT food_type, COUNT(*) AS total_distributions, SUM(quantity) AS total_quantity_distributed
FROM distributions
GROUP BY food_type;

SELECT u.username, COUNT(d.id) AS total_donations
FROM users u
LEFT JOIN donations d ON u.id = d.user_id
GROUP BY u.id;
