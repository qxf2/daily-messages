"""
Unit tests for comment reviewer's endpoint
"""
import main
from unittest.mock import patch
from messages import comments_reviewer
from freezegun import freeze_time

@freeze_time("2021-03-18")
@patch('messages.comments_reviewer.messages',{'2021-03-18':"Today's comment reviewer's are A and B"})
def test_get_comment_reviewers():
    "asserting message as per date"
    message = main.get_comment_reviewers()
    assert message['msg'] == "Today's comment reviewer's are A and B"

@freeze_time("2021-03-29")
@patch('messages.comments_reviewer.messages',{'2021-03-29':"No comment reviewer's for today"})
def test_no_comment_reviewers():
    "asserting message as per date"
    message = main.get_comment_reviewers()
    assert message['msg']=="No comment reviewer's for today"
