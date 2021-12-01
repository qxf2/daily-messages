"""
Endpoints for reminders and daily messages
"""
import datetime
import os
import pickle
import random
from fastapi import FastAPI
from messages import reminders
from messages import senior_qa_training
from messages import comments_reviewer
app = FastAPI()

CURR_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
MESSAGES_PATH = os.path.join(CURR_FILE_PATH, 'messages')
CULTURE_FILE = os.path.join(MESSAGES_PATH, 'culture.txt')
SEP20_INTERNS_FILE = os.path.join(MESSAGES_PATH, 'sep20_interns.txt')
SENIOR_QA_TRAINING_PICKLE = os.path.join(MESSAGES_PATH, 'senior_qa_training.pickle')

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
    "Returns message including comment reviewers names"
    today= get_today_date()
    if today in comments_reviewer.messages.keys():
        lines = comments_reviewer.messages.get(today, [''])
        message = lines
    else:
        message = "Either today is not Thursday or data is not available for this date"

    return {'msg':message}
