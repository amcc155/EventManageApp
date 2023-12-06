-- Drop existing tables if they exist
DROP TABLE IF EXISTS attendees;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS people;

alter TABLE people
alter column dob DATETIME

-- Create 'people' table
CREATE TABLE people (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    address VARCHAR(95),
    email VARCHAR(255),
    dob DATE,
    phone VARCHAR(20),
    role VARCHAR(9)
) ENGINE = INNODB;

-- Insert data into 'people' table
INSERT INTO people (name, address, email, dob, phone, role)
VALUES
    ('John Doe', '123 Main St', 'john.doe@example.com', '1990-01-01', '1234567890', 'customer'),
    ('Jane Smith', '456 Oak Ave', 'jane.smith@example.com', '1985-05-15', '9876543210', 'staff'),
    ('Bob Johnson', '789 Pine Ln', 'bob.johnson@example.com', '1995-08-20', '5551234567', 'customer'),
    ('Alice Williams', '101 Elm St', 'alice.williams@example.com', '1980-03-10', '9998887777', 'staff'),
    ('Charlie Brown', '202 Cedar Rd', 'charlie.brown@example.com', '2000-12-05', '1112223333', 'customer');

-- Create 'venues' table
CREATE TABLE venues (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    address VARCHAR(95),
    phone VARCHAR(20) NOT NULL,
    fee INT,
    maximum_attendees INT
) ENGINE = INNODB;

-- Insert data into 'venues' table
INSERT INTO venues (name, address, phone, fee, maximum_attendees)
VALUES
    ('Grand Hall', '500 Plaza Dr', '555-1234', 1500, 200),
    ('City Gardens', '123 Park St', '555-5678', 800, 100),
    ('Lakeside Manor', '789 Lakeview Dr', '555-9876', 2000, 300),
    ('Skyline Ballroom', '101 Skyway Ave', '555-4321', 2500, 400),
    ('Downtown Loft', '202 Urban Ln', '555-8765', 1200, 150);

-- Create 'events' table
CREATE TABLE events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    event_date DATE,
    start_time TIME,
    end_time TIME,
    invitation VARCHAR(225),
    image_path VARCHAR(100),
    maximum_attendees INT,
    rental_items TEXT,
    notes TEXT,
    planner INT,
    host INT,
    venue INT,
    FOREIGN KEY (planner) REFERENCES people (person_id),
    FOREIGN KEY (host) REFERENCES people (person_id),
    FOREIGN KEY (venue) REFERENCES venues (venue_id)
) ENGINE = INNODB;

-- Insert data into 'events' table
INSERT INTO events (name, event_date, start_time, end_time, venue, invitation, maximum_attendees, planner, host, rental_items, notes, image_path)
VALUES
    ('Birthday Party', '2023-05-20', '18:00:00', '23:00:00', 1, 'You are invited to a birthday celebration!', 50, 2, 3, 'Tables, Chairs, PA System', 'Bring decorations and cake.', 'images/birthday-party.png'),
    ('Dinner Party', '2023-07-15', '19:30:00', '23:30:00', 4, 'Join us for an elegant corporate event!', 300, 4, 1, 'Stage, Lighting, Projector', 'Formal dress code.', 'images/dinner-party.png'),
    ('Graduation', '2023-06-10', '12:00:00', '17:00:00', 2, 'GRADUATION event!', 150, 1, 5, 'Picnic tables, Blankets', 'Bring your favorite dish to share.', 'images/graduation-event.png'),
    ('Outdoor Party', '2023-08-25', '16:00:00', '22:00:00', 3, 'Celebrate the union of John and Jane!', 200, 2, 4, 'Tables, Chairs, Dance Floor', 'RSVP by August 10th.', 'images/outdoor-party.png'),
    ('Sports Event', '2023-09-12', '14:00:00', '18:00:00', 5, 'Introducing our latest product!', 100, 3, 1, 'Presentation setup, Product display', 'Media coverage scheduled.', 'images/sports-event.png');

-- Create 'attendees' table
CREATE TABLE attendees (
    attendee_id INT,
    event_id INT,
    FOREIGN KEY (attendee_id) REFERENCES people (person_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id)
) ENGINE = INNODB;

-- Insert data into 'attendees' table
INSERT INTO attendees (attendee_id, event_id)
VALUES
    (1, 3),
    (2, 4),
    (3, 1),
    (2, 3),
    (4, 3);
