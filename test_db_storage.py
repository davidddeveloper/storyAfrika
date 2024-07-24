#!/usr/bin/python

from models.engine.db_storage import DBStorage
from models.base_model import Base
from models.bookmark import Bookmark
from models.comment import Comment
from models.follower import Follower
from models.like import Like
from models.story import Story
from models.topic_follower import TopicFollower
from models.topic import Topic
from models.user import User


storage = DBStorage()
storage.reload()

user1 = User(
    username='david',
    email='david@gmail.com',
    password='pwd@david@088',
    fullname='David Conteh',
    short_bio='Software Engineer',
    about='I"m a software engineer \
with two decades of experience'
)

user1.set_password(user1.password)
user1.image = 'https://picsum/700/200'

user2 = User(
    username='paul',
    email='paul@gmail.com',
    password='pwd@david@088',
    fullname='Paul Wright',
    short_bio='Enterpreneur | Business man',
    about='I like to share the struggles \
I"m personally face in the business industry'
)

user2.set_password(user2.password)
user2.image = 'https://picsum/500/200'


user3 = User(
    username='alusine',
    email='alusine@gmail.com',
    password='pwd@david@088',
    fullname='Alusine Bangura',
    short_bio='Teacher | Educator',
    about='I like to share how education have transform\
Education have transform the lives of my student'
)

user3.set_password(user3.password)
user3.image = 'https://picsum/300/500'

user4 = User(
    username='alikodangote',
    email='alikodangote@gmail.com',
    password='aliko1234@xyz',
    fullname='Aliko Dangote',
    short_bio='Enterpreneur | Successful Business man'
)

user4.set_password(user4.password)
user4.image = 'https://picsum/500/400'


topic1 = Topic(
    name='Education',
    description='Education is transformative'
)

topic2 = Topic(
    name='Love',
    description='Love is patient and kind. It does not Jealous'
)

topic3 = Topic(
    name='Business',
    description='Business focus on afrika'
)

with open('story_protective_dad.txt', 'r') as st:
    contents = st.read()

story1 = Story(
    title='My dad was protective during the civil ware in SL',
    text=contents,
    user_id=user3.id,
    topics=[topic2]
)

with open('story_aliko_dangote.txt', 'r') as st:
    contents = st.read()

story2 = Story(
    title='My journey to becoming the a successful enterpreneur in Afrika',
    text=contents,
    user_id=user4.id,
    topics=[topic3]
)

like1 = Like(story_id=story2.id, user_id=user2.id)
like2 = Like(story_id=story2.id, user_id=user1.id)
like3 = Like(story_id=story1.id, user_id=user2.id)
like4 = Like(story_id=story2.id, user_id=user3.id)

#follower1 = Follower(user1.id, user4.id)
#follower2 = Follower(user4.id, user3.id)

comment1 = Comment(
    comment="Amazing story! \
I'm truely inspired to know you actually work hard for your money. \
Which is in contrast to what people are saying. Continue doing what you do.",
    story_id=story2.id,
    user_id=user3.id
)

bookmark1 = Bookmark(
    story_id=story1.id,
    user_id=user2.id
)

bookmark2 = Bookmark(
    story_id=story2.id,
    user_id=user2.id
)

storage._session.add_all([user1, user2, user3, user4])
storage._session.add_all([topic1, topic2, topic3])
storage._session.add_all([story1, story2])
storage._session.add_all([like1, like2, like3, like4])
#storage._session.add_all([follower1, follower2])
storage._session.add_all([comment1, bookmark1, bookmark2])

storage.save()
