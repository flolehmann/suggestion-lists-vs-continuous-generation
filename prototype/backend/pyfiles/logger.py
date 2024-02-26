import time
import pandas as pd
import difflib as dl

class InputLogger:
    def __init__(self, tid):
        self.tid = tid
        self.log = pd.DataFrame(columns=['Time', 'Perf_Time', 'Action'])
        self.curr_sen = ''
    
    def get_action(self, old_sen, new_sen):
        if len(new_sen) >= len(old_sen):
            #return new_sen[len(old_sen):]
            d = ''
            for li in dl.ndiff(old_sen, new_sen):
                if li[0] == '+':
                    d += li[-1]
            return d
        elif len(new_sen) < len(old_sen):
            return 'BACK'
        else:
            return ''

    def log_sen(self, sen):
        t = time.localtime()
        ts = ''
        for i in [t.tm_hour, t.tm_min, t.tm_sec]:
            if i < 10:
                ts += '0'
            ts += str(i) + ':'
        ts = ts[:-1]
        perft = time.perf_counter()
        act = self.get_action(self.curr_sen, sen)
        act = act.replace('\n','\\n').replace(';',',')
        if act == ' ':
            act = 'SPACE'
        self.curr_sen = sen
        self.log.loc[len(self.log)] = [ts, perft, act]

    def get_log(self):
        return self.log