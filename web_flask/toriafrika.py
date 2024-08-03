from web_flask.app import app, login, storage
from models.user import User
from models.base_model import Base
from models.bookmark import Bookmark
from models.comment import Comment
from models.follower import Follower
from models.like import Like
from models.story import Story
from models.topic_follower import TopicFollower
from models.topic import Topic
from models.user import User


@login.user_loader
def load_user(id):
    return storage.get(User, id)


# application context in shell
@app.shell_context_processor
def make_shell_context():
    return {
        'User': User,
        'Topic': Topic,
        'Story': Story,
        'Like': Like,
        'Follower': Follower,
        'Comment': Comment,
        'Bookmark': Bookmark,
        'Base': Base,
        'storage': storage
    }


#  @app.before_request
#  def create_new_session():
#      storage.reload()


@app.teardown_appcontext
def shutdown_session(exception=None):
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
