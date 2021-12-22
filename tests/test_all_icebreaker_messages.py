"""
Code level tests for /icebreaker/all endpoint
"""
from unittest.mock import patch
import main
from messages import icebreaker

@patch('messages.icebreaker.messages', ['msg1', 'msg2'])
def test_get_all_icebreaker_message():
    "Test that correct content is returned"
    expected_messages = ['msg1', 'msg2']
    message = main.get_all_icebreaker_message()
    assert message['msg'] == expected_messages

def test_length_all_icebreaker_messages():
    "Verify that /icebreaker/all returns same number of lines as icebreaker.py file"
    lines = icebreaker.messages
    expected_length = len(lines)
    message = main.get_all_icebreaker_message()
    assert len(message.get('msg', [])) == expected_length