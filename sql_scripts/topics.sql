USE storyafrika;

-- Insert Topics
INSERT INTO topics (id, name, created_at, updated_at) VALUES
(uuid(), 'Education', NOW(), NOW()),
(uuid(), 'Resilience', NOW(), NOW()),
(uuid(), 'Innovation', NOW(), NOW()),
(uuid(), 'Art', NOW(), NOW()),
(uuid(), 'Entrepreneurship', NOW(), NOW());
 