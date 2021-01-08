"""
Method for deleting pickle file
"""
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#Declaring directory
REPO_DIR = os.path.dirname(os.path.dirname(__file__))
MESSAGES_DIR = os.path.join(REPO_DIR, 'messages')

# Declaring files to delete
FILE_DELETE = ['senior_qa_training.pickle']

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
    delete_files_in_dir(MESSAGES_DIR, FILE_DELETE)
