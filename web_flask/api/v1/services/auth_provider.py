from models.engine import storage
from models.user import User
from models.story import Story
from models.topic import Topic
from models.comment import Comment
from web_flask.api.v1.services.data_service import get_user_data

current_user = None

def authenticate(email, password):
    user = storage._session.query(User).where(User.email == email).first()

    if user:
        global current_user
        current_user = user
        return get_user_data(user)
    else:
        return False


def authorize(obj=None):
    """
        restrict or give permission to the current user

        Args:
            - obj: can be an instance of any models: User, Story, Comment, Topic
    """
    if not obj:
        return False

    if isinstance(obj, Story):
        story = obj
        if story.writer == current_user or 'admin' in current_user.roles:
            return True
        return False
    
    if isinstance(obj, User):
        user = obj
        if user == current_user or 'admin' in current_user.roles:
            return True
        return False

    if isinstance(obj, Comment):
        comment = obj
        if comment.commenter == current_user or 'admin' in current_user.roles:
            return True
        return False
    
    if isinstance(obj, Topic):
        topic = obj
        if topic.creator == current_user or 'admin' in current_user.roles:
            return True
        return False
