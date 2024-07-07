"""
    routes: all application endpoints

"""

from web_flask.app import app, storage
from flask import render_template
from models.topic import Topic
from models.story import Story
from models.user import User


@app.route("/", strict_slashes=False)
def home():
    all = storage.all()
    topics = storage.all(Topic)
    stories = storage.all(Story)
    print(all)

    return render_template('home.html', all=all, topics=topics, stories=stories)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)