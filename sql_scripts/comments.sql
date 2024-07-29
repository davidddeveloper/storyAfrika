SELECT * FROM storyafrika.comments;
-- Insert Comments
INSERT INTO comments (id, comment, story_id, user_id, created_at, updated_at) VALUES
(uuid(), 'This is an amazing story! It really captures the essence of how education can change lives.', (SELECT id FROM stories WHERE title = 'The Power of Education'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), 'Very inspiring! I am moved by the resilience shown in this story.', (SELECT id FROM stories WHERE title = 'A Journey of Resilience'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW()),
(uuid(), 'Great read! Technology truly is a game-changer in our society.', (SELECT id FROM stories WHERE title = 'Innovating for Change'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW());

-- Insert More Comments
INSERT INTO comments (id, comment, Story, User, created_at, updated_at) VALUES
(uuid(), 'This story is incredibly inspiring and thought-provoking.', (SELECT id FROM stories WHERE title = 'Exploring the Unknown'), (SELECT id FROM users WHERE username = 'john_doe'), NOW(), NOW()),
(uuid(), 'A fascinating read! The Last Frontier captures the essence of adventure.', (SELECT id FROM stories WHERE title = 'The Last Frontier'), (SELECT id FROM users WHERE username = 'jane_doe'), NOW(), NOW()),
(uuid(), 'Innovations in Medicine is an eye-opening look at the future of healthcare.', (SELECT id FROM stories WHERE title = 'Innovations in Medicine'), (SELECT id FROM users WHERE username = 'mary_jane'), NOW(), NOW()),
(uuid(), 'Journey to the Stars is a captivating and inspiring tale of space exploration.', (SELECT id FROM stories WHERE title = 'Journey to the Stars'), (SELECT id FROM users WHERE username = 'peter_parker'), NOW(), NOW()),
(uuid(), 'The Rise of AI raises important questions about the future of technology.', (SELECT id FROM stories WHERE title = 'The Rise of AI'), (SELECT id FROM users WHERE username = 'tony_stark'), NOW(), NOW()),
(uuid(), 'Climate Change Warriors is a powerful call to action for environmental protection.', (SELECT id FROM stories WHERE title = 'Climate Change Warriors'), (SELECT id FROM users WHERE username = 'bruce_wayne'), NOW(), NOW()),
(uuid(), 'The Digital Revolution provides a fascinating look at how technology is changing the world.', (SELECT id FROM stories WHERE title = 'The Digital Revolution'), (SELECT id FROM users WHERE username = 'clark_kent'), NOW(), NOW()),
(uuid(), 'Breaking Barriers is an inspiring story of resilience and determination.', (SELECT id FROM stories WHERE title = 'Breaking Barriers'), (SELECT id FROM users WHERE username = 'diana_prince'), NOW(), NOW()),
(uuid(), 'The Future of Work offers valuable insights into the future of employment.', (SELECT id FROM stories WHERE title = 'The Future of Work'), (SELECT id FROM users WHERE username = 'steve_rogers'), NOW(), NOW()),
(uuid(), 'Art in the Digital Age highlights the innovative use of technology in art.', (SELECT id FROM stories WHERE title = 'Art in the Digital Age'), (SELECT id FROM users WHERE username = 'natasha_romanoff'), NOW(), NOW());
