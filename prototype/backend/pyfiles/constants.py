import os

# Link to survey
SURVEY_LINK = 'https://hciaitools.uni-bayreuth.de/surveys/index.php/377687?lang=en'

# Dir for the Data files
#DATA_DIR = os.getcwd() + '/data'  
DATA_DIR = os.getcwd() + '/real_data'  

# Minimum text length that has to be written in one task (in words)
MIN_TEXT_LENGTH = 20

# The amount of displayed suggestions (for Version2)
AMOUNT_SUGGESTIONS = 3

# The names for the different methods
METHODS = {
    0: 'Standard textfield',
    1: 'Continuous generated text',
    2: 'Writing with suggestions'
}

# The different tasks
TASKS = {
    # Concrete Task
    0: 'It\'s your friend\'s birthday. Write him an email to wish him all the best and mention that you have to meet again in some time.', 
    # Open Task
    1: 'Write a short story about your last or upcoming vacation.'
}

# The questions after each task
QUESTIONS = [
    'I am satisfied with the text.',
    'It was easy for me to write the text.',
    'I feel like I am the author of the text.',
    'The interaction method was suitable for this task.',
    'The interaction method helped me write the text.',
    'The interaction method influenced the wording of the text.'
]

# Header for the Task file
TASK_FILE_HEADER = (
    'taskid;' + 
    'task;' +
    'method;' +
    'result;' + 
    'needed_time;' + 
    'time_generating;' +
    'amount_generations;' +
    'amount_new_opts'
)
for i in range(len(QUESTIONS)):
    TASK_FILE_HEADER += ';question' + str(i)
TASK_FILE_HEADER += '\n'
