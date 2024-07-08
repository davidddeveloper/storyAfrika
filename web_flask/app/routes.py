"""
    routes: all application endpoints

"""

from web_flask.app import app, storage
from web_flask.app.forms import LoginForm, UserRegistrationForm
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from flask import render_template, redirect, url_for, request, flash
from models.topic import Topic
from models.story import Story
from models.user import User
from urllib.parse import urlsplit


@app.route("/", strict_slashes=False)
@login_required
def home():
    """ Home View """
    all = storage.all()
    topics = storage.all(Topic)
    stories = storage.all(Story)

    return render_template(
        'home.html', all=all, topics=topics, stories=stories
    )


@app.route(
    "/login", strict_slashes=False, methods=['GET', 'POST']
)
def login():
    """ Login View """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = storage._session.query(User).filter_by(
            username=form.username.data
        ).first()
        # check if the password is valid
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))

        if user is None or not user.email == form.email.data:
            flash(
                f"No account is associated with this email {form.email.data}",
                "warning"
            )
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page and urlsplit(next_page).netloc != '':
            return redirect(url_for('home'))

        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # save password as hash
        user.set_password(user.password)
        # save user to storage
        storage.new(user)
        storage.save()

        flash(
            f'Registration completed successfully \
            for {user.username}', 'success'
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dummy')
@login_required
def dummy_view():
    return '<h1> What is wrong with you </h1>'
