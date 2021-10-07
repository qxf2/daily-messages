"""
Code level tests for /desk-exercise/all endpoint
"""
from unittest.mock import patch
import main
from messages import desk_exercises

@patch('messages.desk_exercises.messages', ['msg1', 'msg2'])
def test_get_all_desk_exercise_message():
    "Test that correct content is returned"
    expected_messages = ['msg1', 'msg2']
    message = main.get_all_desk_exercise_message()
    assert message['msg'] == expected_messages

def test_length_all_culture_messages():
    "Verify that /desk-exercise/all returns same number of lines as desk_exercises.py file"
    lines = desk_exercises.messages
    expected_length = len(lines)
    message = main.get_all_desk_exercise_message()
    assert len(message.get('msg', [])) == expected_length



