from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .helpers import extract_username, send_welcome_email
from .schema import Story

# Create your views here.
def first_home_page(request):
    stories = Story.objects.order_by('-created_at')
    print('These are the stories', stories)
    return render(request, 'home/first_home.html', context={
        'stories': stories
    })

def story(request):
    return render(request, 'story/story.html')

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.get(email=email)
            if user and user.check_password(password):
                login(request, user)
                messages.success(request, f'Welcome back {user.username}')
                return redirect('/')

        messages.error(request, 'Email or Password is incorrect!')

    return render(request, 'user/login.html', context={
        'form': form
    })

def join_us(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            username = extract_username(user.email)
            if username and User.objects.filter(username=username).exists():
                form.add_error('email', 'A user with this email already exists: {}'.format(user.email))
                return render(request, 'user/registration.html', context={
                    'form': form
                })
            
            user.username = username
            user.save()

            messages.success(request, f'Account created for {user.username}')

            # send email
            # check if the user click on the checkbox to accept us sending weekly emails
            if request.POST.get('newsletter'):
                send_welcome_email(user)

            return redirect('/sign_in')
    
    return render(request, 'user/registration.html', context={
        'form': form
    })


def sign_out(request):
    logout(request)
    messages.info(request, 'Please Login')
    return redirect('/sign_in')


def story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    related_stories = story.get_related_stories(3)
    other_stories_by_writer = story.get_other_stories_by_writer(3)
    similar_writers = story.get_similar_writers(max_results=5)

    return render(request, 'story/story.html', context={
        'story': story,
        'related_stories': related_stories,
        'other_stories_by_writer': other_stories_by_writer,
        'similar_writers': similar_writers
    })