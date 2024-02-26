from pyfiles.constants import QUESTIONS
from pyfiles.datawriter import DataWriter
from pyfiles.taskmanager import fill_tasks

class Model:
    def __init__(self):
        self.curr_task = None
        self.in_task = False

    def set_user_id(self, uid):
        self.tasks = fill_tasks(uid)
        self.datawriter = DataWriter()
        self.datawriter.set_user_id(uid)

    def set_current_task(self, tid):
        self.curr_task = self.tasks[tid]
        self.in_task = True

    def set_no_curr_task(self):
        self.in_task = False
        self.curr_task = None

    def task_to_json(self):
        if self.in_task:
            return self.curr_task.to_json()

    def start_task_timer(self):
        if self.in_task:
            self.curr_task.start_timer()

    def end_task_timer(self):
        if self.in_task:
            self.curr_task.end_timer()
    
    def add_gen_time(self, time):
        if self.in_task:
            self.curr_task.add_generating_time(time)
    
    def increase_new_opts(self):
        if self.in_task:
            self.curr_task.increase_new_opts()
    
    def task_logging(self, sentence):
        if self.in_task:
            self.curr_task.log(sentence)
    
    def get_questions(self):
        return QUESTIONS
    
    def set_task_result(self, result):
        if self.in_task:
            self.curr_task.set_result(result)
    
    def set_task_rating(self, qidx, rating):
        if self.in_task:
            self.curr_task.set_rating(qidx, rating)
    
    def save_task(self, tidx):
        if self.in_task:
            self.datawriter.store_task(self.tasks[tidx])
            #self.datawriter.store_ratings(self.tasks[tidx].ratings)
            self.datawriter.write_log(self.tasks[tidx].id, self.tasks[tidx].logger.get_log())



