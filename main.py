"""
Endpoints for reminders and daily messages
"""
import datetime
import os
import pickle
import random
from datetime import date
from fastapi import FastAPI
from messages import reminders
from messages import senior_qa_training
from messages import comments_reviewer
from messages import desk_exercises
from messages import icebreaker

app = FastAPI()

CURR_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGES_PATH = os.path.join(CURR_FILE_PATH, 'messages')
CULTURE_FILE = os.path.join(MESSAGES_PATH, 'culture.txt')
SEP20_INTERNS_FILE = os.path.join(MESSAGES_PATH, 'sep20_interns.txt')
SENIOR_QA_TRAINING_PICKLE = os.path.join(MESSAGES_PATH, 'senior_qa_training.pickle')
FIRST_REVIEWER_PICKLE = os.path.join(MESSAGES_PATH, 'first_reviewer.pickle')
SECOND_REVIEWER_PICKLE = os.path.join(MESSAGES_PATH, 'second_reviewer.pickle')
DESK_EXERCISES_PICKLE = os.path.join(MESSAGES_PATH, 'desk_exercises.pickle')
ICEBRAKER_PICKLE = os.path.join(MESSAGES_PATH, 'icebreaker.pickle')


def get_pickle_contents(filename):
    "Return the first variable of a pickle file"
    contents = None
    if os.path.exists(filename):
        with open(filename, 'rb') as file_handler:
            contents = pickle.load(file_handler)

    return contents

def update_pickle_contents(filename, content):
    "Update the contents of the pickle file"
    with open(filename, 'wb+') as file_handler:
        pickle.dump(content, file_handler)

def get_desk_exercise_index():
    "Return the exercise index dict"
    exercise_index_dict = get_pickle_contents(DESK_EXERCISES_PICKLE)
    exercise_index_dict = {} if exercise_index_dict is None else exercise_index_dict

    return exercise_index_dict

def set_desk_exercise_index(exercise_index_dict):
    "Update the exercise index dict for desk exercises"
    update_pickle_contents(DESK_EXERCISES_PICKLE, exercise_index_dict)

def get_icebraker_index():
    "Return the exercise index dict"
    icebraker_index_dict = get_pickle_contents(ICEBRAKER_PICKLE)
    icebraker_index_dict = {} if icebraker_index_dict is None else icebraker_index_dict

    return icebraker_index_dict

def set_icebraker_index(icebraker_index_dict):
    "Update the exercise index dict for icebraker exercises"
    update_pickle_contents(ICEBRAKER_PICKLE, icebraker_index_dict)

def get_senior_qa_training_user_index():
    "Return the user index dict"
    user_index_dict = get_pickle_contents(SENIOR_QA_TRAINING_PICKLE)
    user_index_dict = {} if user_index_dict is None else user_index_dict

    return user_index_dict

def set_senior_qa_training_user_index(user_index_dict):
    "Update the user index for the senior QA training messages"
    update_pickle_contents(SENIOR_QA_TRAINING_PICKLE, user_index_dict)

def get_weekday():
    "Return the weekday"
    return datetime.datetime.today().weekday()

def get_today_date():
    "Return today's date"
    return datetime.datetime.today().strftime('%Y-%m-%d')

def get_messages_from_file(filename):
    "Return a list of culture related messages"
    lines = []
    with open(filename, 'r') as file_handler:
        lines = file_handler.readlines()
    lines = [line.strip() for line in lines]

    return lines

def get_first_comment_reviewer_cycle_index():
    "Return cycle index for comment reviewers"
    cycle_index_dict = get_pickle_contents(FIRST_REVIEWER_PICKLE)
    cycle_index_dict = {} if cycle_index_dict is None else cycle_index_dict

    return cycle_index_dict

def set_first_comment_reviewer_cycle_index(cycle_index_dict):
    "Update cycle index for comment reviewers"
    update_pickle_contents(FIRST_REVIEWER_PICKLE, cycle_index_dict)

def get_second_comment_reviewer_cycle_index():
    "Return user index for comment reviewers"
    cycle_index_dict = get_pickle_contents(SECOND_REVIEWER_PICKLE)
    cycle_index_dict = {} if cycle_index_dict is None else cycle_index_dict

    return cycle_index_dict

def set_second_comment_reviewer_cycle_index(cycle_index_dict):
    "Update cycle index for comment reviewers"
    update_pickle_contents(SECOND_REVIEWER_PICKLE, cycle_index_dict)

def get_first_reviewer(cycle1: str = ''):
    "get first reviewer"
    lines = comments_reviewer.first_reviewers
    if cycle1:
        cycle_index_dict = get_first_comment_reviewer_cycle_index()
        reviewer1_index = cycle_index_dict.get(cycle1, 0)
        first_reviewer = lines[reviewer1_index%len(lines)]
        cycle_index_dict[cycle1] = reviewer1_index + 1
        set_first_comment_reviewer_cycle_index(cycle_index_dict)
    else:
        first_reviewer = random.choice(lines).strip()

    return first_reviewer

def get_second_reviewer(cycle2: str = ''):
    "get second reviewer"
    lines = comments_reviewer.second_reviewers
    if cycle2:
        cycle_index_dict = get_second_comment_reviewer_cycle_index()
        reviewer2_index = cycle_index_dict.get(cycle2, 0)
        second_reviewer = lines[reviewer2_index%len(lines)]
        cycle_index_dict[cycle2] = reviewer2_index + 1
        set_second_comment_reviewer_cycle_index(cycle_index_dict)
    else:
        second_reviewer = random.choice(lines).strip()

    return second_reviewer

def get_distinct_reviewers():
    "Getting distinct reviewers"
    first_reviewer = get_first_reviewer()
    second_reviewer = get_second_reviewer()
    message = f"{first_reviewer}, {second_reviewer} are comments reviewers"
    
    return message

@app.get("/")
def index():
    "The home page"
    return {"msg":"This is the endpoint for the home page. /message \
        and /reminder are more useful starting points."}

@app.get("/message")
def get_message():
    "Return a random message"
    lines = get_messages_from_file(CULTURE_FILE)
    message = random.choice(lines)

    return {'msg':message}

@app.get("/culture/all")
def get_all_culture_messages():
    "Return all available culture messages"
    return {'msg':get_messages_from_file(CULTURE_FILE)}

@app.get("/reminder")
def get_reminder():
    "Return a reminder based on day of the week"
    weekday = get_weekday()
    #Note: Monday is 0 and Sunday is 6
    lines = reminders.messages.get(weekday, [''])
    message = "<b>Reminder:</b> " + random.choice(lines)

    return {'msg':message}

@app.get("/sep20-interns")
def get_sep20_message():
    "Return a message for the Sep 2020 internship"
    lines = get_messages_from_file(SEP20_INTERNS_FILE)

    return {'msg': random.choice(lines)}

@app.get("/training")
def get_snior_qa_training_message(user: str = ''):
    "Return a message for senior QA training"
    lines = senior_qa_training.messages
    user_index_dict = {}
    if user:
        user_index_dict = get_senior_qa_training_user_index()
        message_index = user_index_dict.get(user, 0)
        message = lines[message_index%len(lines)]
        user_index_dict[user] = message_index + 1
        set_senior_qa_training_user_index(user_index_dict)
    else:
        message = random.choice(lines)

    return {'msg': message}

@app.get("/comment-reviewers")
def get_comment_reviewers():
    """
    "Returns message including comment reviewers names"
    """
    if date.today().weekday() == 3:
        message = get_distinct_reviewers()
    else:
        message = "Either today is not Thursday or data is not available for this date"

    return {'msg': message}

@app.get("/desk-exercise")
def get_desk_exercise_message(exercise: str = ''):
    "Returns daily-desk exercise message"
    lines = desk_exercises.messages
    message_index_dict = {}
    if exercise:
        exercise_index_dict = get_desk_exercise_index()
        message_index = exercise_index_dict.get(exercise, 0)
        message = lines[message_index%len(lines)]
        exercise_index_dict[exercise] = message_index + 1
        set_desk_exercise_index(exercise_index_dict)
    else:
        message = random.choice(lines)

    return {'msg':message}

@app.get("/desk-exercise/all")
def get_all_desk_exercise_message():
    "Returns all desk-exercise messages"
    lines = desk_exercises.messages

    return {'msg':lines}

@app.get("/icebreaker")
def get_icebreaker_message(ice: str = ''):
    "Returns daily-icebraker exercise message"
    lines = icebreaker.messages
    message_index_dict = {}
    if ice:
        icebraker_index_dict = get_icebraker_index()
        message_index = icebraker_index_dict.get(ice, 0)
        message = lines[message_index%len(lines)]
        icebraker_index_dict[ice] = message_index + 1
        set_icebraker_index(icebraker_index_dict)
    else:
        message = random.choice(lines)

    return {'msg':message}

@app.get("/icebreaker/all")
def get_all_icebreaker_message():
    "Returns all icebraker messages"
    lines = icebreaker.messages

    return {'msg':lines}
