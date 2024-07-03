"""
    app: flask application

"""

from flask import Flask, render_template
from models.engine import storage
from models.topic import Topic
from models.story import Story

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def home():
    all = storage.all()
    topics = storage.all(Topic)
    stories = storage.all(Story)

    return render_template('home.html', all=all, topics=topics, stories=stories)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)