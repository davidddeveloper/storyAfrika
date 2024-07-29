USE storyafrika;

-- Users
INSERT INTO Users (id, username, email, password, short_bio, about, avatar, first_name, last_name, full_name, created_at, updated_at) VALUES
(uuid(), 'amanda', 'amanda@example.com', 'password123', 'Passionate about education.', 'I have been working in education for over a decade.', 'https://unsplash.it/600', 'Amanda', 'Smith', 'Amanda Smith', NOW(), NOW()),
(uuid(), 'benjamin', 'benjamin@example.com', 'password123', 'Tech enthusiast.', 'I love exploring new technologies and their applications.', 'https://unsplash.it/600', 'Benjamin', 'Johnson', 'Benjamin Johnson', NOW(), NOW()),
(uuid(), 'chiamaka', 'chiamaka@example.com', 'password123', 'Entrepreneurial spirit.', 'I started a business in Africa to empower local communities.', 'https://unsplash.it/600', 'Chiamaka', 'Okeke', 'Chiamaka Okeke', NOW(), NOW()),
(uuid(), 'diana', 'diana@example.com', 'password123', 'Art lover.', 'Art has been my passion since childhood.', 'https://unsplash.it/600', 'Diana', 'Nguyen', 'Diana Nguyen', NOW(), NOW()),
(uuid(), 'emeka', 'emeka@example.com', 'password123', 'Social activist.', 'I fight for women’s rights and equality.', 'https://unsplash.it/600', 'Emeka', 'Ibe', 'Emeka Ibe', NOW(), NOW());
-- (Continue this pattern up to user 100)

-- Stories
INSERT INTO Stories (id, title, text, User, created_at, updated_at, image) VALUES
(uuid(), 'The Power of Education', 'Education can transform lives.', '3', NOW(), NOW(), 'https://unsplash.it/600'),
(uuid(), 'A Journey of Resilience', 'The story of a woman overcoming obstacles.', '5', NOW(), NOW(), 'https://unsplash.it/600'),
(uuid(), 'Innovating for Change', 'How technology is changing lives in Africa.', '2', NOW(), NOW(), 'https://unsplash.it/600'),
(uuid(), 'Finding My Passion', 'My journey to becoming an artist.', '4', NOW(), NOW(), 'https://unsplash.it/600'),
(uuid(), 'Building a Business', 'Challenges and triumphs of entrepreneurship.', '3', NOW(), NOW(), 'https://unsplash.it/600');
-- (Continue this pattern up to story 100)

-- Comments
INSERT INTO Comments (id, comment, Story, User, created_at, updated_at) VALUES
(uuid(), 'This is inspiring!', '1', '1', NOW(), NOW()),
(uuid(), 'I can relate to this.', '2', '4', NOW(), NOW()),
(uuid(), 'Great insights!', '3', '2', NOW(), NOW()),
(uuid(), 'Thank you for sharing.', '4', '5', NOW(), NOW()),
(uuid(), 'I love this story!', '5', '3', NOW(), NOW());
-- (Continue this pattern up to comment 100)

-- Likes
INSERT INTO Likes (id, story_id, user_id, created_at, updated_at) VALUES
(uuid(), '1', '1', NOW(), NOW()),
(uuid(), '2', '2', NOW(), NOW()),
(uuid(), '3', '3', NOW(), NOW()),
(uuid(), '4', '4', NOW(), NOW()),
(uuid(), '5', '5', NOW(), NOW());
-- (Continue this pattern up to like 100)

-- Bookmarks
INSERT INTO Bookmarks (id, story_id, user_id, created_at, updated_at) VALUES
(uuid(), '1', '1', NOW(), NOW()),
(uuid(), '2', '2', NOW(), NOW()),
(uuid(), '3', '3', NOW(), NOW()),
(uuid(), '4', '4', NOW(), NOW()),
(uuid(), '5', '5', NOW(), NOW());
-- (Continue this pattern up to bookmark 100)

-- Topics
INSERT INTO Topics (id, name, description, created_at, updated_at) VALUES
(uuid(), 'Women Empowerment', 'Focus on empowering women in various fields.', NOW(), NOW()),
(uuid(), 'Technology', 'Exploring technology and its impact on society.', NOW(), NOW()),
(uuid(), 'Entrepreneurship', 'Supporting new and aspiring entrepreneurs.', NOW(), NOW()),
(uuid(), 'Education', 'The importance of education in development.', NOW(), NOW()),
(uuid(), 'Art and Culture', 'Celebrating art and cultural diversity.', NOW(), NOW());
-- (Continue this pattern up to topic 20)

-- Followers
INSERT INTO Followers (id, follower_id, followed_id, created_at, updated_at) VALUES
(uuid(), '1', '2', NOW(), NOW()),
(uuid(), '1', '3', NOW(), NOW()),
(uuid(), '2', '4', NOW(), NOW()),
(uuid(), '3', '5', NOW(), NOW()),
(uuid(), '4', '1', NOW(), NOW());
-- (Continue this pattern up to follower 200)

-- Comment Likes
INSERT INTO CommentLikes (id, comment_id, user_id, created_at, updated_at) VALUES
(uuid(), '1', '1', NOW(), NOW()),
(uuid(), '2', '2', NOW(), NOW()),
(uuid(), '3', '3', NOW(), NOW()),
(uuid(), '4', '4', NOW(), NOW()),
(uuid(), '5', '5', NOW(), NOW());
-- (Continue this pattern up to comment like 100)

-- Comment Unlikes
INSERT INTO CommentUnlikes (id, comment_id, user_id, created_at, updated_at) VALUES
(uuid(), '1', '2', NOW(), NOW()),
(uuid(), '2', '3', NOW(), NOW()),
(uuid(), '3', '4', NOW(), NOW()),
(uuid(), '4', '5', NOW(), NOW()),
(uuid(), '5', '1', NOW(), NOW());
-- (Continue this pattern up to comment unlike 100)

-- Topic Followers
INSERT INTO TopicFollowers (id, user_id, topic_id, created_at, updated_at) VALUES
(uuid(), '1', '1', NOW(), NOW()),
(uuid(), '2', '2', NOW(), NOW()),
(uuid(), '3', '3', NOW(), NOW()),
(uuid(), '4', '4', NOW(), NOW()),
(uuid(), '5', '5', NOW(), NOW());
-- (Continue this pattern up to topic follower 200)
