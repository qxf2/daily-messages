# daily-messages
A collection of messages, reminders and questions that need to be socialized within Qxf2. The consumers of these endpoints are the training-bot, daily-message-bot and new-hire-bot.

### SETUP

1. Install the requirements `pip install -r requirements.txt`
2. Start the app `uvicorn main:app`
3. To check if the app started, in a new terminal `curl http://127.0.0.1:8000/message`
4. If all goes well, you should see a message displayed

### How to run test

1. Run the command `coverage run -m pytest` for running test cases.
2. To check the coverage, you can run `coverage report`-(Note- As a practice we run the coverage for unit tests only.)
