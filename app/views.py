from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from .helpers import extract_username, send_welcome_email
from .schema import Story, Profile

# Create your views here.
def first_home_page(request):
    stories = Story.objects.order_by('-created_at')
    print('These are the stories', stories)
    return render(request, 'home/first_home.html', context={
        'stories': stories,

    })

def story(request):
    return render(request, 'story/story.html')

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = extract_username(email)
            password = form.cleaned_data['password']

            user = User.objects.get(username=username)
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

    # count unique views
    if request.user.is_authenticated:
        story.unique_views.add(request.user.profile)
    
    # count generic views
    # Story.increment_generic_hit_count(request, story)

    related_stories = story.get_related_stories(3)
    other_stories_by_writer = story.get_other_stories_by_writer(3)
    similar_writers = story.get_similar_writers(max_results=5)

    return render(request, 'story/story.html', context={
        'story': story,
        'related_stories': related_stories,
        'other_stories_by_writer': other_stories_by_writer,
        'similar_writers': similar_writers,
    })

def stories(request):
    stories = Story.objects.order_by('-created_at')
    top_writers = Profile.top_writers
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 2)
    stories = Story.paginate(page_number, page_size, order_by='-created_at')

    bookmarks = None
    if request.user.is_authenticated:
        bookmarks = request.user.profile.bookmarks.all().order_by('-created_at')[:3]

    return render(request, 'home/home.html', context={
        'stories': stories,
        'top_writers': top_writers,
        'bookmarks': bookmarks
    })