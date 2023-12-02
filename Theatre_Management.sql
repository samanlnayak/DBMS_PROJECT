-- Create a new database
CREATE DATABASE IF NOT EXISTS TheaterManagement;
USE TheaterManagement;

CREATE TABLE Theater (
    theater_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT
);
-- Create Movie table
CREATE TABLE Movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    genre VARCHAR(50),
    duration INT,
    theater_id  INT,
    description TEXT,
    FOREIGN KEY (theater_id) REFERENCES Theater(theater_id)
);



-- Create Showtime table
CREATE TABLE Showtime (
    showtime_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    theater_id INT,
    start_time DATETIME,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (theater_id) REFERENCES Theater(theater_id)
);

-- Create Customers table
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20)
);

-- Create Ticket table
CREATE TABLE Ticket (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    showtime_id INT,
    customer_id INT,
    seat_number VARCHAR(10),
    price DECIMAL(8, 2),
    FOREIGN KEY (showtime_id) REFERENCES Showtime(showtime_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);



-- Create Employee table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    position VARCHAR(50),
    theater_id INT,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    FOREIGN KEY (theater_id) REFERENCES Theater(theater_id)
);

-- Create TicketCounter table
CREATE TABLE TicketCounters (
    ticket_counter_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    theater_id INT,
    FOREIGN KEY (theater_id) REFERENCES Theater(theater_id)
);

-- Create User table
CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) UNIQUE,
    Password VARCHAR(50),
    Privileges ENUM('admin', 'standard') DEFAULT 'standard'
);

-- Insert into User table
INSERT INTO User (Username, Password, Privileges)
VALUES
    ('saman', 'saman@123', 'admin');




-- Insert data into Theater table
INSERT INTO Theater (name, location, capacity) VALUES
    ('Cineplex Downtown', '123 Main St, Cityville', 5),
    ('Regal Cinemas', '456 Oak St, Townsville', 150),
    ('AMC Theatres', '789 Elm St, Villagetown', 180),
    ('Grand Cinema', '1st Avenue, Metropolis', 220),
    ('Silver Screen', 'Broadway St, Entertainment City', 170),
    ('Cityplex', '3rd Street, Urbanville', 190),
    ('Starlight Cinemas', 'Sunset Blvd, Skyline', 160),
    ('MegaPlex', 'Central Ave, Megatown', 250);
    
-- Insert data into Movie table
INSERT INTO Movie (title, release_date, genre, duration, description,theater_id) VALUES
    ('Saving Private Ryan', '1998-07-24', 'Action', 120, 'A gripping World War II action film',1),
    ('Inception', '2010-07-16', 'Sci-Fi', 150, 'Mind-bending sci-fi thriller directed by Christopher Nolan',8),
    ('The Shawshank Redemption', '1994-09-23', 'Drama', 142, 'Classic drama following Andy Dufresnes journey of hope',3),
    ('The Dark Knight', '2008-07-18', 'Action', 152, 'Christopher Nolans Batman sequel introducing the Joker,',2),
    ('Forrest Gump', '1994-07-06', 'Drama', 142, 'Heartwarming drama chronicling the extraordinary life of Forrest Gump',1),
    ('Pulp Fiction', '1994-10-14', 'Crime', 154, 'Quentin Tarantinos cult crime classic with interconnected stories',6),
    ('The Matrix', '1999-03-31', 'Sci-Fi', 136, ' Groundbreaking sci-fi film following Neo, a hacker',5),
    ('The Godfather', '1972-03-24', 'Crime', 175, 'Francis Ford Coppolas cinematic masterpiece portraying the Corleone crime ',2);

-- Insert data into Showtime table
INSERT INTO Showtime (movie_id, theater_id, start_time) VALUES
    (1, 1, '2023-11-17 18:00:00'),
    (2, 2, '2023-11-18 20:30:00'),
    (3, 3, '2023-11-19 15:45:00'),
    (4, 4, '2023-11-20 17:30:00'),
    (5, 5, '2023-11-21 19:15:00'),
    (6, 6, '2023-11-22 21:00:00'),
    (7, 7, '2023-11-23 14:30:00'),
    (8, 8, '2023-11-24 16:45:00');

-- Insert data into Ticket table

-- Insert data into Customers table
INSERT INTO Customers (first_name, last_name, email, phone) VALUES
    ('John', 'Doe', 'john.doe@example.com', '555-123-4567'),
    ('Jane', 'Smith', 'jane.smith@example.com', '555-987-6543'),
    ('Bob', 'Johnson', 'bob.johnson@example.com', '555-111-2222'),
    ('Alice', 'Williams', 'alice.williams@example.com', '555-333-4444'),
    ('Charlie', 'Brown', 'charlie.brown@example.com', '555-555-6666'),
    ('David', 'Jones', 'david.jones@example.com', '555-777-8888'),
    ('Eva', 'White', 'eva.white@example.com', '555-999-0000'),
    ('Frank', 'Miller', 'frank.miller@example.com', '555-222-3333');
    
INSERT INTO Ticket (showtime_id, customer_id, seat_number, price) VALUES
    (1, 1, 'A1', 10.00),
    (1, 1, 'A2', 10.00),
    (1, 1, 'A3', 10.00),
    (1, 1, 'A4', 10.00),
    (1, 1, 'A5', 10.00),
    (2, 2, 'B2', 12.00),
    (3, 3, 'C3', 11.50),
    (4, 4, 'D4', 14.00),
    (5, 5, 'E5', 13.50),
    (6, 6, 'F6', 15.00),
    (7, 7, 'G7', 12.50),
    (8, 8, 'H8', 16.00);



-- Insert data into Employees table
INSERT INTO Employees (first_name, last_name, position, theater_id, email, phone) VALUES
    ('Manager1', 'Lastname1', 'Manager', 1, 'manager1@example.com', '555-111-1111'),
    ('Seller1', 'Lastname2', 'Seller', 2, 'seller1@example.com', '555-222-2222'),
    ('Cleaner1', 'Lastname3', 'Cleaner', 3, 'cleaner1@example.com', '555-333-3333'),
    ('Usher1', 'Lastname4', 'Usher', 4, 'usher1@example.com', '555-444-4444'),
    ('Supervisor1', 'Lastname5', 'Supervisor', 5, 'supervisor1@example.com', '555-555-5555'),
    ('Cashier1', 'Lastname6', 'Cashier', 6, 'cashier1@example.com', '555-666-6666'),
    ('Security1', 'Lastname7', 'Security', 7, 'security1@example.com', '555-777-7777'),
    ('Tech1', 'Lastname8', 'Tech Support', 8, 'tech1@example.com', '555-888-8888');

-- Insert data into TicketCounters table
INSERT INTO TicketCounters (name, theater_id) VALUES
    ('Counter 1', 1),
    ('Counter 2', 1),
    ('Counter 3', 1),
    ('Counter 1', 2),
    ('Counter 1', 3),
    ('Counter 2', 3),
    ('Counter 1', 4),
    ('Counter 1', 5),
    ('Counter 1', 6),
    ('Counter 2', 6),
    ('Counter 1', 7),
    ('Counter 1', 8);
    
DELIMITER //

CREATE TRIGGER after_insert_movie 
AFTER INSERT ON Movie
FOR EACH ROW
BEGIN
  -- Insert into Showtime only for the specified theaters
  INSERT IGNORE INTO Showtime (movie_id, theater_id, start_time) 
  SELECT NEW.movie_id, t.theater_id, CURDATE() + INTERVAL 1 DAY
  FROM Theater t
  WHERE t.theater_id = NEW.theater_id;
END;
//
DELIMITER ;
DELIMITER $$

CREATE PROCEDURE GetMovieInformation(
  IN p_movie_id INT
)
BEGIN
  SELECT *
  FROM Movie
  WHERE movie_id = p_movie_id;
END $$

DELIMITER ;
DELIMITER //

CREATE TRIGGER before_insert_ticket
BEFORE INSERT ON Ticket
FOR EACH ROW
BEGIN
  DECLARE theater_capacity INT;
  DECLARE sold_tickets INT;

  -- Get the capacity of the theater for the associated showtime
  SELECT capacity INTO theater_capacity
  FROM Theater
  WHERE theater_id = (SELECT theater_id FROM Showtime WHERE showtime_id = NEW.showtime_id);

  -- Get the number of tickets already sold for the showtime
  SELECT COUNT(*) INTO sold_tickets
  FROM Ticket
  WHERE showtime_id = NEW.showtime_id;

  -- Check if the theater is full
  IF sold_tickets >= theater_capacity THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Theater is full. Cannot sell more tickets for this showtime.';
  END IF;
END;
//
DELIMITER ;


SELECT title from Movie
WHERE release_date =1998-07-24;

SELECT
    M.title AS MovieTitle,
    SUM(T.price) AS TotalCollections
FROM
    Movie M
JOIN
    Showtime S ON M.movie_id = S.movie_id
JOIN
    Ticket T ON S.showtime_id = T.showtime_id
WHERE
    M.title = 'The Dark Knight'
GROUP BY
    M.title;


INSERT INTO Ticket (showtime_id, customer_id, seat_number, price) VALUES
(4,9,'H11',100.00);