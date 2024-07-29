USE storyafrika;

-- Insert Users
INSERT INTO users (id, username, email, password, first_name, last_name, full_name, created_at, updated_at) VALUES
(uuid(), 'aminabello', 'amina@example.com', 'password123', 'Amina', 'Bello', 'Amina Bello', NOW(), NOW()),
(uuid(), 'chiamaka89', 'chiamaka@example.com', 'password123', 'Chiamaka', 'Igwe', 'Chiamaka Igwe', NOW(), NOW()),
(uuid(), 'yusuf_teacher', 'yusuf@example.com', 'password123', 'Yusuf', 'Abdullah', 'Yusuf Abdullah', NOW(), NOW());

-- Insert More Users
INSERT INTO users (id, username, email, password, first_name, last_name, full_name, created_at, updated_at) VALUES
(uuid(), 'john_doe', 'john.doe@example.com', 'password456', 'John', 'Doe', 'John Doe', NOW(), NOW()),
(uuid(), 'jane_doe', 'jane.doe@example.com', 'password456', 'Jane', 'Doe', 'Jane Doe', NOW(), NOW()),
(uuid(), 'mary_jane', 'mary.jane@example.com', 'password456', 'Mary', 'Jane', 'Mary Jane', NOW(), NOW()),
(uuid(), 'peter_parker', 'peter.parker@example.com', 'password456', 'Peter', 'Parker', 'Peter Parker', NOW(), NOW()),
(uuid(), 'tony_stark', 'tony.stark@example.com', 'password456', 'Tony', 'Stark', 'Tony Stark', NOW(), NOW()),
(uuid(), 'bruce_wayne', 'bruce.wayne@example.com', 'password456', 'Bruce', 'Wayne', 'Bruce Wayne', NOW(), NOW()),
(uuid(), 'clark_kent', 'clark.kent@example.com', 'password456', 'Clark', 'Kent', 'Clark Kent', NOW(), NOW()),
(uuid(), 'diana_prince', 'diana.prince@example.com', 'password456', 'Diana', 'Prince', 'Diana Prince', NOW(), NOW()),
(uuid(), 'steve_rogers', 'steve.rogers@example.com', 'password456', 'Steve', 'Rogers', 'Steve Rogers', NOW(), NOW()),
(uuid(), 'natasha_romanoff', 'natasha.romanoff@example.com', 'password456', 'Natasha', 'Romanoff', 'Natasha Romanoff', NOW(), NOW());
