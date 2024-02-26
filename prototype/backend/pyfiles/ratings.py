# ------------------------------
# This is the backend part for 
# the questions after each task
# ------------------------------
from pyfiles.constants import QUESTIONS


class Ratings:
    def __init__(self, tid):
        self.tid = tid
        self.ratings = [0 for i in range(len(QUESTIONS))]
    
    def set_rating(self, quest, rating):
        self.ratings[quest] = rating

    def to_csv(self):
        s = ''
        for rating in self.ratings:
            s += str(rating) + ';'
        return s[:-1]