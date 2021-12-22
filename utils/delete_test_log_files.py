"""
Method for deleting pickle file
"""
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Declaring directory
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
MESSAGES_DIR = os.path.join(REPO_DIR, 'messages')
TESTS_DIR = os.path.join(REPO_DIR, 'tests')

# Declaring files to delete
PICKLE_FILE_DELETE = ['senior_qa_training.pickle']
DESK_EXERCISES_PICKLE = ['desk_exercises.pickle']
PACT_JSON = ['qxf2_employee_messages_lambda-qxf2_daily_messages_microservices.json']

# Delete file
def delete_file(file_name):
    """
    This method will delete a particular file
    """
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f'{file_name} deleted')

# Delete files from particular directory
def delete_files_in_dir(directory, files):
    "The method will delete files in a particular directory"
    for file_name in files:
        delete_file(os.path.join(directory, file_name))

# Delete pickle file
def delete_pickle_file():
    "The method will delete pickle file"
    delete_files_in_dir(MESSAGES_DIR, PICKLE_FILE_DELETE)

# Delete json file
def delete_pact_json_file():
    "This method will delete pact json file"
    delete_files_in_dir(TESTS_DIR, PACT_JSON)

# Delete desk exercise pickle file
def delete_desk_exercise_pickle():
    "This method will delete desk exercise file"
    delete_files_in_dir(MESSAGES_DIR, DESK_EXERCISES_PICKLE)