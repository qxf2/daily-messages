"""
Contract test for daily messages
"""
import random
import logging
import atexit
import unittest
import pytest
import requests
from pact import Consumer, Provider, Format
from messages import reminders
import main

# Declaring logger
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
print(Format().__dict__)

pact = Consumer('Qxf2 employee messages lambda').\
    has_pact_with(Provider('Qxf2 daily messages microservices'))
pact.start_service()
atexit.register(pact.stop_service)

class Getmessage(unittest.TestCase):
    """
    Defining Test class contract test
    """
    def test_get_index(self):
        """
        Defining test for /index endpoint
        """
        expected = {
        'msg' : 'This is the endpoint for the home page. /message    \
            and /reminder are more useful starting points.'
        }

        (pact\
        . given('Request to get home page') \
        . upon_receiving('a request for home page')\
        . with_request('GET', '/')\
        . will_respond_with(200, body=expected))\

        with pact:\
            result = requests.get(pact.uri + '/')\

        self.assertEqual(result.json(), expected)
        pact.verify()

    def test_get_message(self):
        """
        Defining test for /message endpoint
        """
        lines = []
        with open(main.CULTURE_FILE, 'r') as fileprocess:
            lines = fileprocess.readlines()
        message = random.choice(lines)
        expected = {
        'msg': message.strip()\
        }
        (pact
        . given('Request to get message') \
        . upon_receiving('a request for get message')\
        . with_request('GET', '/message')\
        . will_respond_with(200, body=expected))\

        with pact:\
            result = requests.get(pact.uri + '/message')\

        self.assertEqual(result.json(), expected)
        pact.verify()

    def test_get_reminder(self):
        """
        Defining test for /reminder endpoint
        """
        weekday = main.get_weekday()
        lines = reminders.messages.get(weekday, [''])
        message = "<b>Reminder:</b> " + random.choice(lines)
        expected = {
        'msg': message.strip()
        }
        (pact
        . given('Request to get reminder') \
        . upon_receiving('a request for reminder')\
        . with_request('GET', '/reminder')\
        . will_respond_with(200, body=expected))\

        with pact:\
            result = requests.get(pact.uri + '/reminder')\

        self.assertEqual(result.json(), expected)
        pact.verify()

    def test_get_sep20_message(self):
        """
        Defining test for /sep20-interns endpoint
        """
        lines = []
        with open(main.SEP20_INTERNS_FILE, 'r') as fileprocess:
            lines = fileprocess.readlines()
        expected = {
        'msg': random.choice(lines).strip()
        }
        (pact
        . given('Request to sep20 interns') \
        . upon_receiving('a request to sep20 interns')\
        . with_request('GET', '/sep20-interns')\
        . will_respond_with(200, body=expected))\

        with pact:\
            result = requests.get(pact.uri + '/sep20-interns')\

        self.assertEqual(result.json(), expected)
        pact.verify()
