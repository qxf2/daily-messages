"""
Test for main page using fastapi test client.
"""
import datetime
import os
import sys
from unittest.mock import patch
from fastapi.testclient import TestClient
from freezegun import freeze_time
import main
from main import app
from messages import reminders
from messages import senior_qa_training
from messages import comments_reviewer
from messages import desk_exercises
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Declaring test client
client = TestClient(app)

# Test case for index page
def test_index():
    "asserting main endpoint"
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["msg"] != ''
    assert response.json() == {"msg":"This is the endpoint for the home page. /message \
        and /reminder are more useful starting points."}

# Test for status code for get message
def test_get_message():
    "asserting status code"
    response = client.get("/message")
    assert response.status_code == 200

# Test for asserting random message is in the file
def test_get_message_text():
    "asserting random message is in the file"
    response = client.get("/message")
    message = response.json()
    assert response.json()["msg"] != ''
    with open(main.CULTURE_FILE, 'r') as file_handler:
        lines = [line.strip() for line in file_handler]
    assert message['msg'] in lines

# Test for Reminders status code
def test_get_reminder():
    "asserting status code"
    response = client.get("/reminder")
    assert response.status_code == 200

# Test for asserting correct reminder sent
def test_get_reminder_text_check():
    "asserting message from the file"
    response = client.get("/reminder")
    message = response.json()
    assert response.json()["msg"] != ''
    weekday = main.get_weekday()
    lines = reminders.messages.get(weekday, [''])
    message = message.get('msg', '')
    message = message.split('Reminder:</b>')[-1].lstrip()
    assert message in lines

# Test for sep20_interns status code
def test_get_sep20_message():
    "asserting status code"
    response = client.get("/sep20-interns")
    assert response.status_code == 200

# Test for asserting correct message for sep20_interns
def test_get_sep20_message_text_check():
    "asserting message from the file"
    response = client.get("/sep20-interns")
    message = response.json()
    assert response.json()["msg"] != ''
    with open(main.SEP20_INTERNS_FILE, 'r') as file_handler:
        lines = [line.strip() for line in file_handler]
    assert message['msg'] in lines

# Test for trainig status code
def test_get_trainig():
    "asserting status code"
    response = client.get("/training")
    assert response.status_code == 200

# Test for asserting message with senior_qa_training messages
def test_get_senior_qa_training_message_text_check():
    "asserting message text check"
    response = client.get("/training")
    message = response.json()
    assert response.json()["msg"] != ''
    lines = senior_qa_training.messages
    assert message['msg'] in lines

# Test for checking first message shown after first cycle is completed.
@patch('messages.senior_qa_training.messages', ['msg1', 'msg2'])
@patch('main.get_senior_qa_training_user_index')
def test_get_senior_training_unique_message(mock_get_index):
    "Test that the senior QA training messages cycle"
    mock_get_index.return_value = {'Qxf2':0}

    result = main.get_snior_qa_training_message('Qxf2')
    assert result['msg'] == 'msg1', f"{result['msg']}"

    result = main.get_snior_qa_training_message('Qxf2')
    assert result['msg'] == 'msg2', f"{result['msg']}"

    result = main.get_snior_qa_training_message('Qxf2')
    assert result['msg'] == 'msg1', f"{result['msg']}"

# Test for checking first message shown after first cycle is completed for /desk-exercise endpoint
@patch('messages.desk_exercises.messages', ['msg1', 'msg2'])
@patch('main.get_desk_exercise_index')
def test_get_desk_exercise_message(mock_get_index):
    "Test desk exercise messages cycle"
    mock_get_index.return_value = {'exercise':0}

    result = main.get_desk_exercise_message('exercise')
    assert result['msg'] == 'msg1', f"{result['msg']}"

    result = main.get_desk_exercise_message('exercise')
    assert result['msg'] == 'msg2', f"{result['msg']}"

    result = main.get_desk_exercise_message('exercise')
    assert result['msg'] == 'msg1', f"{result['msg']}"

# Test for comment-reviewers status code
def test_get_comments():
    "asserting status code"
    response = client.get("/comment-reviewers")
    assert response.status_code == 200

# Test for checking message
def test_get_comment_reviewers():
    "asserting message as per date"
    response = client.get("/comment-reviewers")
    message = response.json()
    assert response.json()["msg"] != ''
    today= main.get_today_date()
    if today in comments_reviewer.messages.keys():
        lines = comments_reviewer.messages.get(today, [''])
        assert message['msg'] in lines
        print(message['msg'])
    else:
        print(f'For {today} there is no comment reviewer message')
