"""
Code level tests for /culture/all endpoint
"""
from unittest.mock import patch
import main

@patch('main.get_messages_from_file')
def test_get_all_culture_messages(mock_obj):
    "Test that /message gets the right content"
    print("\n")
    test_msg_1 = "Hello! This is unit test message 1!"
    test_msg_2 = "Hello! This is unit test message 2!"
    expected_messages = [test_msg_1, test_msg_2]
    mock_obj.return_value = expected_messages
    message = main.get_all_culture_messages()
    assert message.get('msg', '') == expected_messages, "Something fishy. /culture/all is NOT returning all messages from get_messages_from_file"

def test_length_all_culture_messages():
    "Verify that /culture/all returns same number of lines as CULTURE FILE"
    with open(main.CULTURE_FILE, 'r') as file_handler:
        lines = file_handler.readlines()
    expected_length = len(lines)
    message = main.get_all_culture_messages()
    assert len(message.get('msg', [])) == expected_length, "/culture/all is returning a different number of lines that in CULTURE FILE"