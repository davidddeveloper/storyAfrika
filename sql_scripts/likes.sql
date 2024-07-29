USE storyafrika;

-- Insert Likes
INSERT INTO likes (id, story_id, user_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM stories WHERE title = 'The Power of Education'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'A Journey of Resilience'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Innovating for Change'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW());

-- Insert More Likes
INSERT INTO likes (id, story_id, user_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM stories WHERE title = 'Exploring the Unknown'), (SELECT id FROM users WHERE username = 'john_doe'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'The Last Frontier'), (SELECT id FROM users WHERE username = 'jane_doe'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Innovations in Medicine'), (SELECT id FROM users WHERE username = 'mary_jane'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Journey to the Stars'), (SELECT id FROM users WHERE username = 'peter_parker'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'The Rise of AI'), (SELECT id FROM users WHERE username = 'tony_stark'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Climate Change Warriors'), (SELECT id FROM users WHERE username = 'bruce_wayne'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'The Digital Revolution'), (SELECT id FROM users WHERE username = 'clark_kent'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Breaking Barriers'), (SELECT id FROM users WHERE username = 'diana_prince'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'The Future of Work'), (SELECT id FROM users WHERE username = 'steve_rogers'), NOW(), NOW());
