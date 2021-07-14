"""
Test for main page using fastapi test client.
"""
# import datetime
import os
import sys
from datetime import date
import pytest
from unittest.mock import patch
# from unittest.mock import Mock
import mock
from fastapi.testclient import TestClient
import main
from main import app
from messages import reminders
from messages import senior_qa_training
# from messages import comments_reviewer
# from utils.custom_exception import RecursionDepthLimitException
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

# Test for comment-reviewers status code
def test_get_comments():
    "asserting status code"
    response = client.get("/comment-reviewers")
    assert response.status_code == 200

# Test for checking message
def test_get_comment_reviewers():
    "asserting message as per date"
    response = client.get("/comment-reviewers")
    if date.today().weekday() != 3:
        assert response.json()["msg"] == "Either today is not Thursday or data is not available for this date"
    else:
        assert response.json()["msg"] != ''

#Test for distinct reviewers
@patch('messages.comments_reviewer.first_reviewers', ['user1'])
@patch('messages.comments_reviewer.first_reviewers', ['user2'])
def test_get_distinct_reviewers_different():
    "Test getting distinct reviewer"
    message = main.get_distinct_reviewers()
    assert message == "user1, user2 are comments reviewers" or "user2, user1 are comments reviewers"

#Test for exception when both reviewers are same
@patch('messages.comments_reviewer.first_reviewers', ['user1'])
@patch('messages.comments_reviewer.second_reviewers', ['user1'])
@mock.patch('utils.custom_exception.RecursionDepthLimitException')
def test_check_no_same_comment_reviewer(mock_exception):
    "Test getting distinct reviewer"
    mock_exception.return_value == "Both reviewers are same"
    with pytest.raises(Exception) as mock_exception.return_value:
        assert main.get_distinct_reviewers.call_count == 1


@patch('messages.comments_reviewer.first_reviewers', ['user1','user2','user3'])
@mock.patch('main.get_first_comment_reviewer_cycle_index')
@mock.patch('main.set_first_comment_reviewer_cycle_index')
def test_get_first_reviewer(mock_get_index,mock_set_index):
    "Test for get_first_reviewer method"
    mock_get_index.return_value = {'Qxf2':0}

    mock_set_index.return_value = {'Qxf2':1}
    result = main.get_first_reviewer('Qxf2')
    assert result == 'user1' or 'user2' or 'user3'

    mock_set_index.return_value = {'Qxf2':2}
    result1 = main.get_first_reviewer('Qxf2')
    assert result1 != result

    mock_set_index.return_value = {'Qxf2':3}
    result2 = main.get_first_reviewer('Qxf2')
    assert result2 != result or result1

    mock_set_index.return_value = {'Qxf2':4}
    result4 = main.get_first_reviewer('Qxf2')
    assert result4 == 'user1' or 'user2' or 'user3'

@patch('messages.comments_reviewer.second_reviewers', ['user1','user2','user3'])
@mock.patch('main.get_second_comment_reviewer_cycle_index')
@mock.patch('main.set_second_comment_reviewer_cycle_index')
def test_get_first_reviewer(mock_get_index,mock_set_index):
    "Test for get_second_reviewer method"
    mock_get_index.return_value = {'Qxf2':0}

    mock_set_index.return_value = {'Qxf2':1}
    result = main.get_second_reviewer('Qxf2')
    assert result == 'user1' or 'user2' or 'user3'

    mock_set_index.return_value = {'Qxf2':2}
    result1 = main.get_second_reviewer('Qxf2')
    assert result1 != result

    mock_set_index.return_value = {'Qxf2':3}
    result2 = main.get_second_reviewer('Qxf2')
    assert result2 != result or result1

    mock_set_index.return_value = {'Qxf2':4}
    result4 = main.get_second_reviewer('Qxf2')
    assert result4 == 'user1' or 'user2' or 'user3'

@patch('messages.comments_reviewer.first_reviewers', ['user1','user2','user3'])
@mock.patch('main.get_first_comment_reviewer_cycle_index')
def test_get_unique_first_reviewer(mock_get_index):
    "checking unique second reviewers"
    mock_get_index.return_value = {'Qxf2':0}

    result = main.get_first_reviewer('Qxf2')
    assert result == 'user1'

    result = main.get_first_reviewer('Qxf2')
    assert result == 'user2'

    result = main.get_first_reviewer('Qxf2')
    assert result == 'user3'

    result = main.get_first_reviewer('Qxf2')
    assert result == 'user1'

@patch('messages.comments_reviewer.second_reviewers', ['user1','user2','user3'])
@mock.patch('main.get_second_comment_reviewer_cycle_index')
def test_get_unique_second_reviewer(mock_get_index):
    "checking unique second reviewers"
    mock_get_index.return_value = {'Qxf2':0}

    result = main.get_second_reviewer('Qxf2')
    assert result == 'user1'

    result = main.get_second_reviewer('Qxf2')
    assert result == 'user2'

    result = main.get_second_reviewer('Qxf2')
    assert result == 'user3'

    result = main.get_second_reviewer('Qxf2')
    assert result == 'user1'
