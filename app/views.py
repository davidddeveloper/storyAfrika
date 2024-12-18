from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView
from django.db.models import Q
from .schema import EmailList
from .forms import LoginForm, RegistrationForm
from .helpers import extract_username, send_welcome_email, serialize_url
from .schema import Story, Profile, FeaturingStory, Topic
import json

# Create your views here.
def first_home_page(request):
    stories = Story.objects.filter(status='p').order_by('-created_at')

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

            user = get_object_or_404(User, email=email)
            print(user)
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
            user.newsletter_opt_in = form.cleaned_data['newsletter_opt_in']
            user.save()

            messages.success(request, f'Account created for {user.username}')

            # send email
            # check if the user click on the checkbox to accept us sending weekly emails
            if request.POST.get('newsletter_opt_in'):
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

def story_view(request, story_title):
    
    
    result = serialize_url(story_title)
    title = result[0]
    writer = result[1]

    user = User.objects.get(username=writer)
    profile = Profile.objects.get(user=user)

    story = Story.objects.filter(title__contains=title, writer=profile.id).first()
    print(story)
    if story.writer != profile:
        print('nope exiting')
        raise ValueError('exitting...')
    
    return HttpResponse(f'<h1> {story.title}</h1>')

def stories(request):
    stories = Story.objects.filter(status='p').order_by('-created_at')
    top_writers = Profile.top_writers
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 6)
    stories = Story.paginate(page_number, page_size, order_by='-created_at')

    featuring_story = FeaturingStory.objects.filter(status='a').first()

    bookmarks = None
    if request.user.is_authenticated:
        bookmarks = request.user.profile.bookmarks.all().order_by('-created_at')[:3]

    return render(request, 'home/home.html', context={
        'stories': stories,
        'top_writers': top_writers,
        'bookmarks': bookmarks,
        'featuring_story': featuring_story
    })

@csrf_exempt
@require_POST
def subscribe(request):
    data = json.loads(request.body)
    email = data.get('email').strip() if data.get('email') else ''
    if not email or '@' not in email:
        return JsonResponse({'error': 'Invalid email address'}, status=400)

    try:
        new_email = EmailList(email=email)
        new_email.save()
        return JsonResponse({'message': 'Successfully subscribed!', 'success': True}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# password Reset

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'emails/password_reset_email.html'
    subject_template_name = 'emails/password_reset_subject.txt'
    success_url = 'done'



def like_story(request, story_id=None):
    story = get_object_or_404(Story, id=story_id)
    print(story.likes.count())
    story.likes.add(request.user.profile)

    return JsonResponse({"ok": True, "love_count": story.love_count}, status=200)


def unlike_story(request, story_id=None):
    story = get_object_or_404(Story, id=story_id)
    story.likes.remove(request.user.profile)

    return JsonResponse({"ok": True, "love_count": story.love_count}, status=200)

def search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    print(query)
    if category == 'stories':
        stories = Story.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        return render(request, 'home/search.html', {'stories': stories, 'query': query})
    elif category == 'topics':
        topics = Topic.objects.filter(name__icontains=query)
        return render(request, 'home/search.html', {'topics': topics, 'query': query})
    elif category == 'people':
        profiles = Profile.objects.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
        return render(request, 'home/search.html', {'profiles': profiles, 'query': query})
    else:
        return render(request, 'home/search.html')
