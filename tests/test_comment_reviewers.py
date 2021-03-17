"""
Code level tests for comment reviewer's endpoint
"""
import datetime
from unittest.mock import patch
import main
from messages import comments_reviewer
from freezegun import freeze_time

@freeze_time("2021-03-18")
def test_get_comment_reviewers():
    "asserting message as per date"
    today = "2021-03-18"
    print(today)
    message = main.get_comment_reviewers()
    lines = comments_reviewer.messages.get(today, [''])
    assert message['msg'] in lines
    print(message['msg'])

@freeze_time("2021-03-29")
def test_no_comment_reviewers():
    "asserting message as per date"
    today = "2021-03-29"
    print(today)
    message = main.get_comment_reviewers()
    assert message['msg']=="Either today is not Thursday or data is not available for this date"
    print(message['msg'])
