"""
    routes: all application endpoints

"""

from sqlalchemy.orm import joinedload
from web_flask.app import app, send_welcome_email, storage
from web_flask.app.forms import LoginForm, UserRegistrationForm, UserUpdateForm
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from flask import render_template, redirect, url_for, request, flash, \
    abort, send_from_directory, jsonify
from models.topic import Topic
from models.story import Story
from models.user import User
from urllib.parse import urlparse
from flask import session, make_response
from werkzeug.utils import secure_filename
import os
import imghdr
import requests



base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)

@app.route("/", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def home():
    """
    Endpoint for the homepage. This endpoint handles both get and post requests
    It is only accessible to logged in users.

    If a post request is made, it checks if there is a file in the request and
    updates the user's avatar if it is a valid image. If the file is not an image,
    or if the request does not contain a file, the file is ignored.

    If the request contains a form, the form is validated and the user's
    username, email or password is updated if the form is valid.

    If the form is not valid, the errors are printed to the console.

    If a get request is made, or if the form is not valid, the page is rendered
    with the current user's data, all users, topics, stories, and stories the
    current user is following.
    """
    if not current_user.registration_finish:
        return redirect(url_for('complete_registration'))

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
            
            if form.first_name:
                if current_user.first_name != form.first_name.data:
                    current_user.first_name = form.first_name.data
                    flash("First Name changed!")

            if form.last_name:
                if current_user.last_name != form.last_name.data:
                    current_user.last_name = form.last_name.data
                    flash("Last Name changed!")
            
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


@app.route('/search', methods=['GET'], strict_slashes=False)
def search():
    return render_template('search.html')

@app.route('/edit-profile', methods=['POST'], strict_slashes=False)
def edit_profile():
    if not current_user.registration_finish:
        return redirect(url_for('complete_registration'))

    form = UserUpdateForm()
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
        
        if form.first_name.data:
            if current_user.first_name != form.first_name.data:
                current_user.first_name = form.first_name.data
                flash("First Name changed!")

        if form.last_name.data:
            if current_user.last_name != form.last_name.data:
                current_user.last_name = form.last_name.data
                flash("Last Name changed!")
        
        if form.short_bio.data:
            if current_user.short_bio != form.short_bio.data:
                current_user.short_bio = form.short_bio.data
                flash("Bio changed successfully")
        
        if form.about.data:
            if current_user.about != form.about.data:
                current_user.about = form.about.data
                flash("About changed successfully")
        current_user.save()
        storage.save()
    else:
        print(form.errors)

    return redirect(request.referrer)


@app.route(
        "/story/<string:story_id>/", strict_slashes=False, methods=['GET', 'POST']
)
def story(story_id=None):
    """
    story: renders a story page

        - story_id: the uuid of the story

    """
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    return render_template('story.html', story=story)


@app.route(
    "/story/write/", strict_slashes=False, methods=['GET', 'POST']
)
def write():
    """
    write: renders a write page

        - GET: renders a blank page to write a story
        - POST: saves the story with the given image
    """
    if not current_user.registration_finish:
        return redirect(url_for('complete_registration'))

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
    """
    login: renders a login page

        - GET: renders a login form
        - POST: checks if the given credentials are valid, if they are, logs the
            user in and redirects them to the next page
    """
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
            next_page = url_for('home')

        # generate a jwttoken
        response = requests.post('http://127.0.0.1:4000/api/v1/auth', json={
            "email": f"{form.email.data}",
            "password": f"{form.password.data}"
        }, headers={
            'Content-Type': 'application/json'
        },)
        
        token = response.json()
        print(token)
        response =  make_response(redirect(next_page))
        response.set_cookie('jwt_token', token.get('data'))

        return response
    
    else:
        print('>>>>>', form.errors)

    response = make_response(render_template('login.html', form=form))
    response.set_cookie('test', 'xyz')
    return response


@app.route('/logout')
def logout():
    """
    logout user and redirect to login page
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    register user

    renders a registration form on GET request
    processes the form data on POST request
    saves the user to the database and redirects to login page
    """
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

        # set default profile image
        user.set_default_profile()

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
    if not current_user.registration_finish:
        redirect(url_for('complete_registration'))

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

@app.route(
    '/test_html/'
)
def test_html():
    return render_template('skeletons/story_card.html')

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route("/api/v1/stories/<string:story_id>/upload_image/", methods=['OPTIONS', 'POST'], strict_slashes=False)
def upload_image_for_story(story_id=None):
    if story_id is None:
         abort(404)

    story = storage.get(Story, story_id)
    if story is None:
         abort(404)

    if request.files:
            try:
                # save the file
                path_2_file = story.image_upload(request.files['file'], auth.current_user.id)
            except Exception:
                return jsonify({"Error": "Failed to upload image"})
            if path_2_file:
                story.image = path_2_file
                storage.save()
            return jsonify(story.to_dict()), 200
    print(request.files)
    return ({}), 400



@app.route(
    '/topic/<string:name>/',
    methods=['GET'],
    strict_slashes=False
)
def topic(name=None):
    """
    Endpoint to render a topic page.

    Parameters:
        name (str): The name of the topic to render.

    Returns:
        The rendered HTML page.

    Raises:
        404: If the topic is not found.
    """
    if not current_user.registration_finish:
        return redirect(url_for('complete_registration'))

    if name is None:
        abort(404)

    topic = storage._session.query(Topic).where(Topic.name==name).first()
    if topic is None:
        abort(404)

    #contributors = storage._session.query(User).where(User.id.in_(topic.contributors)).all()
    return render_template('topic/topic.html', topic=topic)

@app.route(
    '/profile/<string:username>/',
    methods=['GET'],
    strict_slashes=False
)
def profile(username=None):
    """
    Endpoint to render a topic page.

    Parameters:
        name (str): The name of the topic to render.

    Returns:
        The rendered HTML page.

    Raises:
        404: If the topic is not found.
    """
    if not current_user.registration_finish:
        return redirect(url_for('complete_registration'))

    form = UserUpdateForm()

    if username is None:
        abort(404)

    username = username[1:] if username.startswith('@') else username

    user = storage._session.query(User).where(User.username == username).first()
    if user is None:
        abort(404)

    return render_template('user/profile.html', user=user, form=form)

@app.route('/login_with_google/', methods=['POST'], strict_slashes=False)
def login_with_google():
    # Retrieve token from the request
    """
    Endpoint to handle a login attempt with a Google token.

    Request should contain a JSON payload with a single key-value pair:
    {
        "token": <string>
    }

    The function verifies the token with Google's API, extracts user information
    from the response, and checks if the user exists in the database. If the user
    exists, they are logged in. If the user doesn't exist, a new user is created
    with the extracted information and logged in.

    :return:
        A JSON response with a single key-value pair:
        {
            "success": <bool>
        }
        If the login is successful, the "success" key has a value of True. If
        the login fails, the value is False, and an optional "message" key
        contains a string with an error message.
    :rtype:
        tuple
    """
    token = request.json.get('token')
    
    # Verify the token with Google's API
    try:
        # Google token verification endpoint
        response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': token}
        )
        user_info = response.json()
        # If the token is invalid, return an error
        if 'error_description' in user_info:
            return jsonify({'success': False, 'message': 'Invalid token'}), 400

        # Extract user information
        google_id = user_info['sub']  # Google unique user ID
        email = user_info['email']
        name = user_info['name']
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')
        username = first_name + (last_name if last_name else '')
        username = username.lower()
        temporary_password = 'fake-password'
        picture = user_info['picture']

        # Check if the user exists in the database
        user = storage._session.query(User).where(User.email==email).first()

        if user:
            # User exists, log them in
            login_user(user, remember=True)
        else:
            # Create a new user
            user = User(email=email, username=username, first_name=first_name, last_name=last_name, avatar=picture)
            user.set_password(temporary_password)
            user.save()
            login_user(user, remember=True)

        # generate a jwttoken
        response = requests.post('http://127.0.0.1:4000/api/v1/auth', json={
            "email": user.email,
            "password": temporary_password,
        }, headers={
            'Content-Type': 'application/json'
        },)

        token = response.json()

        response = make_response(jsonify({'success': True, 'redirect_url': url_for('home')}))
        response.set_cookie('jwt_token', token.get('data'))
        send_welcome_email(user.email, user.first_name)
        return response

    except Exception as e:
        print(f"Error during Google login: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500


@app.route('/complete_registration/', methods=['GET', 'POST'], strict_slashes=False)
def complete_registration():
    if current_user.registration_finish:
        return redirect('/')
    if request.method == 'POST':
        # capture first name and last name data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if first_name and last_name:
            current_user.first_name = first_name
            current_user.last_name = last_name
            #current_user.registration_complete = True
            storage.save()
            #return redirect(url_for('home'))
        
        # capture which topics the user is interested in
        topics = request.form.getlist('topics')
        if topics:
            current_user.topics = [storage._session.query(Topic).where(Topic.name == topic).first() for topic in topics]
            current_user.registration_finish = True
            storage.save()
            # return redirect(url_for('home'))
        
        # # capture which users the user is interested in following
        # users = request.form.getlist('users')
        # if users:
        #     for user in users:
        #         user_to_follow = storage._session.query(User).where(User.username == user).first()
        #         if user_to_follow:
        #             current_user.following.add(user_to_follow)
        #     storage.save()
            return jsonify({"message": "registration completed successful", "success": True, "redirect_url": url_for('home')})
        else:
            return redirect(url_for('complete_registration'))

    topics = storage._session.query(Topic).limit(10).all()
    users_suggestions = storage._session.query(User).join(User.topics).where(Topic.id.in_(map(lambda x: x.id, topics))).limit(8).all()
    #contributor_ids = [contributor.id for contributor in topics[0].contributors]  

    #users_suggestions = storage._session.query(User).where(User.id.in_(contributor_ids)).limit(4).all()
    send_welcome_email(current_user.email, current_user.first_name)
    return render_template("complete-registration.html", topics=topics, users_suggestions=users_suggestions)
