from actions import amount_actions_user
from backs import amount_backs_user, backsequs_user
from constants import USER_IDS, task_file, log_file, boxplot_by_method, avg_by_method, count_by_methods
from generationeval import generations_user, new_options_user, amount_chosen_options_user
from wpm import textlen_user

if __name__ == '__main__':
    methods = [
        amount_backs_user,
        backsequs_user,
        amount_actions_user,
        generations_user,
        new_options_user
        #amount_chosen_options_user
    ]
    count_by_methods(methods)