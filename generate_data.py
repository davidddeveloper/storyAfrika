import os
import uuid
import datetime
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models
from models.base_model import Base
from models.user import User
from models.topic import Topic
from models.story import Story
from models.comment import Comment
from models.like import Like
from models.follower import Follower
from models.bookmark import Bookmark
from models.topic_follower import TopicFollower

# Database connection details
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'story_afrika'

# Set the storage environment variable
os.environ['STORAGE'] = 'db'

# Create an engine and session
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Generate fake data
fake = Faker()

# Number of records to create
NUM_USERS = 100
NUM_TOPICS = 20
NUM_STORIES = 200
NUM_COMMENTS = 500
NUM_LIKES = 500
NUM_FOLLOWERS = 200
NUM_BOOKMARKS = 300
NUM_TOPIC_FOLLOWERS = 150

def create_users():
    users = []
    for _ in range(NUM_USERS):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            short_bio=fake.sentence(),
            about=fake.paragraph()
        )
        users.append(user)
    session.bulk_save_objects(users)
    session.commit()

def create_topics():
    topics = []
    for _ in range(NUM_TOPICS):
        topic = Topic(
            name=fake.word(),
            description=fake.sentence()
        )
        topics.append(topic)
    session.bulk_save_objects(topics)
    session.commit()

def create_stories():
    users = session.query(User).all()
    topics = session.query(Topic).all()
    stories = []
    for _ in range(NUM_STORIES):
        story = Story(
            title=fake.sentence(),
            text=fake.text(),
            user_id=fake.random_element(users).id,
            topics_id=[fake.random_element(topics).id for _ in range(fake.random_int(min=1, max=3))]  # Select 1 to 3 random topics
        )
        stories.append(story)
    session.bulk_save_objects(stories)
    session.commit()

def create_comments():
    users = session.query(User).all()
    stories = session.query(Story).all()
    comments = []
    for _ in range(NUM_COMMENTS):
        comment = Comment(
            comment=fake.sentence(),  # Ensure the 'comment' field is populated
            story_id=fake.random_element(stories).id,
            user_id=fake.random_element(users).id
        )
        comments.append(comment)
    session.bulk_save_objects(comments)
    session.commit()

def create_likes():
    users = session.query(User).all()
    stories = session.query(Story).all()
    likes = []
    for _ in range(NUM_LIKES):
        like = Like(
            story_id=fake.random_element(stories).id,
            user_id=fake.random_element(users).id
        )
        likes.append(like)
    session.bulk_save_objects(likes)
    session.commit()

def create_followers():
    users = session.query(User).all()
    followers = []
    for _ in range(NUM_FOLLOWERS):
        follower = Follower(
            follower_id=fake.random_element(users).id,
            followed_id=fake.random_element(users).id
        )
        followers.append(follower)
    session.bulk_save_objects(followers)
    session.commit()

def create_bookmarks():
    users = session.query(User).all()
    stories = session.query(Story).all()
    bookmarks = []
    for _ in range(NUM_BOOKMARKS):
        bookmark = Bookmark(
            story_id=fake.random_element(stories).id,
            user_id=fake.random_element(users).id
        )
        bookmarks.append(bookmark)
    session.bulk_save_objects(bookmarks)
    session.commit()

def create_topic_followers():
    users = session.query(User).all()
    topics = session.query(Topic).all()
    topic_followers = []
    for _ in range(NUM_TOPIC_FOLLOWERS):
        topic_follower = TopicFollower(
            user_id=fake.random_element(users).id,
            topic_id=fake.random_element(topics).id
        )
        topic_followers.append(topic_follower)
    session.bulk_save_objects(topic_followers)
    session.commit()

def main():
    Base.metadata.create_all(engine)
    # create_comments()
    create_topic_followers()
    print("Data generation complete!")

if __name__ == "__main__":
    main()


