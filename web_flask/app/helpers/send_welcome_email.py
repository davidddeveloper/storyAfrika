def send_welcome_email(user_email, first_name):
    with app.app_context():
        subject = "Welcome to StoryAfrika!"
        body = f"""
        Hi {first_name},

        Welcome to StoryAfrika! We’re excited to have you join our community. Here at StoryAfrika, we share inspiring stories from across Africa, focusing on success stories and the journeys behind them. From entrepreneurs and artists to everyday heroes, we cover how they achieved their goals and overcame challenges.

        With StoryAfrika, you can:
        - Read stories that motivate and inspire.
        - Share your own success stories or journeys.
        - Connect with a community of like-minded individuals.

        We hope you enjoy your journey with us and look forward to your contributions and engagement!

        Best Regards,
        The StoryAfrika Team
        """

        msg = Message(subject, recipients=[user_email])
        msg.body = body
        mail.send(msg)
