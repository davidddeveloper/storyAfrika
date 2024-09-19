"""
    routes: all application endpoints

"""

from sqlalchemy.orm import joinedload
from web_flask.app import app, storage
from web_flask.app.forms import LoginForm, UserRegistrationForm, UserUpdateForm
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from flask import render_template, redirect, url_for, request, flash, \
    abort, send_from_directory
from models.topic import Topic
from models.story import Story
from models.user import User
from urllib.parse import urlparse
from flask import session
from werkzeug.utils import secure_filename
import os
import imghdr



base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)

@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def home():
    """ Home View """
    form = UserUpdateForm()

    if request.method == 'POST':
        if request.files:
            try:
                # save the file
                path_2_file = current_user.image_upload(request.files['file'], current_user.id)
            except Exception:
                path_2_file = None

            if path_2_file is not None:
                current_user.avatar = path_2_file
                storage.save()
        
        if form.validate_on_submit():
            # change password
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                flash("Password change!")

            if form.username.data:  # update the username
                if current_user.username != form.username.data:
                    current_user.username = form.username.data
                    flash("Username changed!")
            
            if form.email.data:  # update the email
                if current_user.email != form.email.data:
                    current_user.email = form.email.data
                    flash("Email changed!")
            
            storage.save()
        else:
            print(form.errors)

    # all = storage.all()
    topics = storage.all(Topic)
    users = storage.all(User)
    stories = storage.all(Story)
    following_stories = storage._session.scalars(current_user.following_stories).all()

    return render_template(
        'home.html', users=users, topics=topics, stories=stories, following_stories=following_stories, form=form
    )


@app.route(
        "/story/<string:story_id>/", strict_slashes=False, methods=['GET', 'POST']
)
def story(story_id=None):
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    return render_template('story.html', story=story)


@app.route(
    "/story/write/", strict_slashes=False, methods=['GET', 'POST']
)
def write():
    if request.method == 'POST':
        story = storage.get(Story, request.form.get('story_id'))
        if request.files:
            try:
                # save the file
                path_2_file = story.image_upload(request.files['file'], current_user.id)
            except Exception:
                path_2_file = None
            if path_2_file is not None:
                story.image = path_2_file
                storage.save()
                print(story.image)
            else:
                flash("Please try an image with a different format.")
                return url_for('write')
            return url_for('write', story=story)

    return render_template('write.html', topics=storage.all(Topic))


@app.route(
    "/login", strict_slashes=False, methods=['GET', 'POST']
)
def login():
    """ Login View """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    print('_________________^^__________', current_user)
    if form.is_submitted:
        print(form.username.data)
        print(form.email.data)
        print(form.password.data)
        #print('csrf token from form', form.csrf_token.data)
        print('csrf token from session', dict(session))
    print(form.validate_on_submit())
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

        if not next_page and urlparse(next_page).netloc != ''\
                and urlparse(next_page).hostname\
                != urlparse(request.url).hostname:
            # not a relative path and not from my domain
            return redirect(url_for('home'))

        return redirect(next_page)
    else:
        print('>>>>>', form.errors)

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


@app.route(
    '/immersive_read/<string:story_id>/',
    methods=['GET'],
    strict_slashes=False
)
def immersive_read(story_id=None):
    """ Immersive read 
    
        - story_id: id of the story
    """
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    return render_template('immersive-read.html', story=story)

@app.route('/dummy', methods=['GET', 'POST'])
@login_required
def dummy_view():
    if request.method == 'POST':
        for uploaded_file in request.files.getlist('file'):
            filename = secure_filename(uploaded_file.filename)
            if filename:
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)
                upload_dir = os.path.join(app.config['UPLOAD_PATH'], current_user.get_id())
                os.makedirs(upload_dir, exist_ok=True)
                uploaded_file.save(os.path.join(upload_dir, filename))
        print('OK!')

    try:
        print(os.path.join(app.config['UPLOAD_PATH'], current_user.get_id()))
        files = os.listdir(os.path.join(app.config['UPLOAD_PATH'], current_user.get_id()))
        
    except FileNotFoundError:
        files = []
    print(files)
    return render_template('dummy.html', files=files)

@app.route(
    '/uploads/<string:filename>/<string:user_id>/',
    methods=['GET'],
    strict_slashes=False
)
def upload(filename, user_id):
    # user_dir = os.path.join(app.config['UPLOAD_PATH'], current_user.get_id())
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user_dir = os.path.join(app.config['UPLOAD_PATH'], user.get_id())
    return send_from_directory(user_dir, filename)

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')



