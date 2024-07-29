USE storyafrika;

-- Insert TopicFollowers
INSERT INTO topic_followers (id, topic_id, user_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM topics WHERE name = 'Education'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW()),
(uuid(), (SELECT id FROM topics WHERE name = 'Resilience'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM topics WHERE name = 'Innovation'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW()),
(uuid(), (SELECT id FROM topics WHERE name = 'Art'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM topics WHERE name = 'Entrepreneurship'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW());
