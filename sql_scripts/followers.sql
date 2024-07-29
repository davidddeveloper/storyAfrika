USE storyafrika;

-- Insert Followers
INSERT INTO followers (id, follower_id, followed_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM users WHERE username = 'aminabello'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW()),
(uuid(), (SELECT id FROM users WHERE username = 'chiamaka89'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM users WHERE username = 'yusuf_teacher'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW());
