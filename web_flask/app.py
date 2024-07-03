"""
    app: flask application

"""

from flask import Flask, render_template
from models.engine import storage


app = Flask(__name__)

@app.route("/", strict_slashes=False)
def home():
    all = storage.all()
    return render_template('home.html', all=all)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)