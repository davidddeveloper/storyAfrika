from flask import request, jsonify, abort, url_for
from models.engine import storage
import web_flask.api.v1.services.auth_provider as auth

def get_story_data(story):
    from models.comment import Comment
    from models.like import Like
    from web_flask.api.v1.helper_func import create_uri

    data = {
        **story.to_dict(),
        'comments_count': storage._session.query(Comment).where(
            Comment.story_id == story.id
        ).count(),
        'likes_count': storage._session.query(Like).where(
            Like.story_id == story.id
        ).count(),

        'liked': auth.current_user.liked_story(story.id),
        'bookmarked': auth.current_user.bookmarked_story(story.id),
        'user_is_following_writer': auth.current_user.is_following(story.writer),
        'topics': [create_uri(get_topic_data(topic), 'get_topic') for topic in story.topics],
        
        'links': {
            'make_comment': url_for('views.make_comment_on_story', story_id=story.id),
            'relevant_comments': url_for('views.get_relevant_comments_for_story', story_id=story.id),
            'newest_comments': url_for('views.get_newest_comments_for_story', story_id=story.id),
            'comments': url_for('views.get_comments_for_story', story_id=story.id)

        }
    }

    return data

def get_topic_data(topic):
    data = {
        **topic.to_dict(),
        'links': {
            'followers': url_for('views.get_followers_for_topic', topic_id=topic.id),
            'stories': url_for('views.get_stories_for_topic', topic_id=topic.id),
            'foryou_stories': url_for('views.foryou_stories', topic_id=topic.id)
        }
    }

    return data

def get_user_data(user):
    data = {
        **user.to_dict(),
        'followers_count': auth.current_user.followers_count if auth.current_user else None,
        'following_count': auth.current_user.following_count if auth.current_user else None,
        'stories_written_count': auth.current_user.stories_written_count,
        'links': {
            'stories_written': url_for('views.get_story_of_user'),
            'followers': url_for('views.get_user_followers'),
            'following': url_for('views.get_user_following')
        }
    }

    return data

def get_comment_data(comment):
    data = {
        **comment.to_dict(),
        'is_liked_by': comment.is_liked_by(auth.current_user.id),
        'user_is_following_commenter': auth.current_user.is_following(comment.commenter)
    }

    return data
