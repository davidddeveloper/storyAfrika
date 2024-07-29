USE storyafrika;

-- Insert CommentLikes
INSERT INTO comment_likes (id, comment_id, user_id, created_at, updated_at) VALUES
(uuid(), (SELECT id FROM comments WHERE comment = 'This is an amazing story! It really captures the essence of how education can change lives.'), (SELECT id FROM users WHERE username = 'chiamaka89'), NOW(), NOW()),
(uuid(), (SELECT id FROM comments WHERE comment = 'Very inspiring! I am moved by the resilience shown in this story.'), (SELECT id FROM users WHERE username = 'aminabello'), NOW(), NOW()),
(uuid(), (SELECT id FROM comments WHERE comment = 'Great read! Technology truly is a game-changer in our society.'), (SELECT id FROM users WHERE username = 'yusuf_teacher'), NOW(), NOW());
