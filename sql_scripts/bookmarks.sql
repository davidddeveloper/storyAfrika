USE storyafrika;

-- Insert Bookmarks
INSERT INTO bookmarks (id, story_id, user_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM stories WHERE title = 'The Power of Education'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'A Journey of Resilience'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW()),
(uuid(), (SELECT id FROM stories WHERE title = 'Innovating for Change'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW());
