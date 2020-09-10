"""
Test for main page using fastapi test client.
"""
import os
import sys
from fastapi.testclient import TestClient
import main
import messages
from main import app
from messages import reminders
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
