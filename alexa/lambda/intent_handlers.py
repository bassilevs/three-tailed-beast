import requests
import logging
import random

from enum import Enum
from s3_controller import *
from helper_phrases import *
from constants import API_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConversationState(Enum):
    CREATE_STORY_READ_OLD_CHOICE_STATE = "CREATE_STORY_READ_OLD_CHOICE_STATE"
    READING_OLD_STORY_STATE = "READING_OLD_STORY_STATE"
    CHOOSING_OLD_STORY_STATE = "CHOOSING_OLD_STORY_STATE"
    CREATING_STORY_STATE = "CREATING_STORY_STATE"
    SAVING_STORY_STATE = "SAVING_STORY_STATE"
    NAMING_STORY_STATE = "NAMING_STORY_STATE"


class StateHandler(object):

    def handle_query_intent(self, attributes, user_input, user_id=None):
        return "Couldn't understand what you want, try again"

    def handle_stop_intent(self, attributes):
        return "Couldn't understand what you want, try again"

    def handle_yes_intent(self, attributes):
        return "Couldn't understand what you want, try again"
        
    def handle_no_intent(self, attributes):
        return "Couldn't understand what you want, try again"

    def handle_lunch_intent(self, attributes):
        return "Couldn't understand what you want, try again"
        
    def handle_create_intent(self, attributes):
        return "Couldn't understand what you want, try again"


class CreateStoryReadOldChoiceStateHandler(StateHandler):

    def handle_query_intent(self, attributes, user_input, user_id=None):
        if user_input in user_create_choices:
            attributes['state'] = ConversationState.CREATING_STORY_STATE.name
            attributes['story'] = ""
            response_text = "Let's create a tale together! To end the story say 'finish'. Say the first three words"
            return response_text
        if user_input in user_read_choices:
            stories_list = list_user_stories(user_id)
            attributes['state'] = ConversationState.CHOOSING_OLD_STORY_STATE.name
            response_text = "Choose a story: " + ", ".join(stories_list)
            return response_text
        return "Hmm.. To create new tale say 'create new', to read old ones " \
               "say 'read' or 'read old tales'"
    
    def handle_create_intent(self, attributes):
        attributes['state'] = ConversationState.CREATING_STORY_STATE.name
        attributes['story'] = ""
        response_text = "Let's create a tale together! To end the story say 'finish'. Say the first three words"
        return response_text
        
    def handle_no_intent(self, attributes):
        clear_session(attributes)
        return "Ok, bye then!"
        
    def handle_yes_intent(self, attributes):
        return "Cool! To create a new tale say 'create new', to read old ones " \
               "say 'read' or 'read old tales'"


class ReadingOldStoryStateHandler(StateHandler):
    
    def handle_create_intent(self, attributes):
        attributes['state'] = ConversationState.CREATING_STORY_STATE.name
        attributes['story'] = ""
        response_text = "Let's create a tale together! To end the story say 'finish'. Say the first three words"
        return response_text


class ChoosingOldStoryStateHandler(StateHandler):

    def handle_query_intent(self, attributes, user_input, user_id=None):
        stories_list = list_user_stories(user_id)
        if user_input in stories_list:
            attributes['state'] = ConversationState.CREATE_STORY_READ_OLD_CHOICE_STATE.name
            story = get_story_text(user_id, user_input).decode('utf-8')
            response_text = "Here goes the story: '" + story + "' \n <p>What would you like to do next, create new story or read the old ones?</p>"
            return response_text
        response_text = "Couldn't find story named " + user_input + ". choose from these: " + ", ".join(stories_list)
        return response_text

    def handle_create_intent(self, attributes):
        attributes['state'] = ConversationState.CREATING_STORY_STATE.name
        attributes['story'] = ""
        response_text = "Let's create a tale together! To end the story say 'finish'. Tell me the first three words"
        return response_text


class CreatingStoryStateHandler(StateHandler):

    def handle_query_intent(self, attributes, user_input, user_id=None):
        if len(user_input.split(' ')) != 3:
            return "Please enter exactly three words"
            
        story = attributes.get('story', '')
        new_story = story + " " + user_input

        prediction = ''
        try:
            r = requests.post(API_URL, json={'data': new_story})
            logger.info("Device API result: {}".format(r))
            prediction = r.json()['data']
        except:
            return "There was a problem connecting to the service"

        attributes['story'] = new_story + prediction
        rand_phrase = continue_phrases[random.randint(0, len(continue_phrases) - 1)]
        return "'" + prediction + "' <p>" + rand_phrase + "</p>"

    def handle_stop_intent(self, attributes):
        attributes['state'] = ConversationState.SAVING_STORY_STATE.name
        response = "Your story so far: <p>'" + attributes['story'] + ".'</p> <p>Would you like to save it?</p>"
        return response


class SavingStoryStateHandler(StateHandler):

    def handle_yes_intent(self, attributes):
        attributes['state'] = ConversationState.NAMING_STORY_STATE.name
        response_text = "What would you like to name it?"
        return response_text
        
    def handle_no_intent(self, attributes):
        clear_session(attributes)
        attributes['state'] = ConversationState.CREATE_STORY_READ_OLD_CHOICE_STATE.name
        response_text = "Alright. What would you like to do next, create new story or read the old ones?"
        return response_text


class NamingStoryStateHandler(StateHandler):

    def handle_query_intent(self, attributes, user_input, user_id=None):
        save_story(user_id, user_input, attributes['story'])
        attributes['state'] = ConversationState.CREATE_STORY_READ_OLD_CHOICE_STATE.name
        response_text = "Your story is saved under name - '" + user_input + "'. <p>What would you like to do next, create new story or read the old ones?</p>"
        return response_text
    
    def handle_no_intent(self, attributes):
        clear_session(attributes)
        attributes['state'] = ConversationState.CREATE_STORY_READ_OLD_CHOICE_STATE.name
        response_text = "Alright then, I'll save it under the name 'Untitled'" + 3 + "<p>What would you like to do next, create new story or read the old ones?</p>"
        return response_text


class StatelessStateHandler(StateHandler):

    def handle_lunch_intent(self, attributes):
        attributes['state'] = ConversationState.CREATE_STORY_READ_OLD_CHOICE_STATE.name
        response_text = "Welcome, would you like to create new story or read the old ones?"
        return response_text


state_handlers = {
    "CREATE_STORY_READ_OLD_CHOICE_STATE": CreateStoryReadOldChoiceStateHandler(),
    "READING_OLD_STORY_STATE": ReadingOldStoryStateHandler(),
    "CHOOSING_OLD_STORY_STATE": ChoosingOldStoryStateHandler(),
    "CREATING_STORY_STATE": CreatingStoryStateHandler(),
    "SAVING_STORY_STATE": SavingStoryStateHandler(),
    "NAMING_STORY_STATE": NamingStoryStateHandler(),
    "STATELESS": StatelessStateHandler()
}


def handle_query_intent(attributes, user_input, user_id=None):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_query_intent(attributes, user_input, user_id)


def handle_finish_intent(attributes):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_stop_intent(attributes)


def handle_yes_intent(attributes):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_yes_intent(attributes)


def handle_no_intent(attributes):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_no_intent(attributes)


def handle_lunch_request(attributes):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_lunch_intent(attributes)


def handle_create_intent(attributes):
    state = attributes.get('state', 'STATELESS')
    return state_handlers[state].handle_create_intent(attributes)


def clear_session(attrs):
    attrs = {}
