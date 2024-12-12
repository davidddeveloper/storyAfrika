from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def extract_username(email):
    """
        This function extract the username from the email
    """
    return email.split("@")[0]


def send_welcome_email(user):
    subject = 'Welcome to StoryAfrika'
    text_content = f'Hi {user.username},\n\nThank you for joining us on StoryAfrika. \n\n Here is your account details: \n\nUsername: {user.username} \nEmail: {user.email}, sign in at https://story-afrika.com if you haven not done so. \n\n Here is what to expect from us: \n\n1. We will send you a story every week. \n2. We will send you a story every month. \n3. We will send you a story every quarter. \n\n We are glad to have you here with us {user.username},\n\n Best,\nDavid'
    from_email = 'david@storyafrika.live'
    recipient_list = [user.email]
    html_content = render_to_string('emails/new_welcome_email.html', context={"user": user})

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")

    msg.send(fail_silently=False)

def serialize_url(text: str) -> str:
        # remove username
        idx = 0
        for l in text:
            idx += 1
            if l == "-":
                break

        writer = text[:idx-1]
        title_with_dashes = text[idx:]
        title = title_with_dashes.replace("-"," ")

        return [title, writer]