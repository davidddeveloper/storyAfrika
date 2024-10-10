import web_flask.api.v1.services.auth_provider as auth
from sqlalchemy.orm import joinedload
from flask import request, jsonify, abort
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.services.auth_guard import auth_guard
from web_flask.api.v1.services.data_service import get_story_data, get_topic_data, get_user_data
from web_flask.api.v1.services.data_service import get_comment_data
from models.story import Story
from models.user import User
from models.comment import Comment
from models.like import Like
from models.bookmark import Bookmark
from models.topic import Topic
from web_flask.api.v1 import storage
from web_flask.api.v1.services.gemini import model



@views.route('/ai_assistive_writing', methods=['GET'], strict_slashes=False)
@auth_guard
def ai_assistive_writing():
    """
        Handle assistive writing with Gemini
    """
    action = request.args.get('ask-ai')
    text = request.args.get('text')
    
    # List of valid actions
    actions = ['make-shorter', 'make-longer', 'correct-grammars']

    if action in actions:
        # Craft instruction based on the action
        instruction = f'Please {action.replace("-", " ")} the following text: "{text}". Only {action.replace("-", " ")} the text, and do not add any explanations, comments, or clarifications.'
        
        if action == 'make-longer':
            instruction += " The response must not exceed 100 words."

        # Generate content
        response = model.generate_content(f'{instruction}')
        try:
            response_text = response.text
        except Exception:
            return jsonify({'error': 'something went wrong'}), 400

        # Extract the generated text from the response
        return jsonify({'response': response_text}), 200
    else:
        return jsonify({'response': 'Invalid action'}), 400
    