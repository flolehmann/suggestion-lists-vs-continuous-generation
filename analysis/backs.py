from constants import USER_IDS, DATA_DIR, task_file, log_file, boxplot_by_method, avg_by_method
from wpm import textlen_user
import pandas as pd

def amount_backs_user_task(uid, tid):
    df = log_file(uid, tid)
    values = df['Action'].value_counts()
    if 'BACK' in values:
        return df['Action'].value_counts()['BACK']
    else:
        return 0

def amount_backs_user(uid):
    df = task_file(uid)

    def get_amount(row):
        return amount_backs_user_task(uid, row.name)
    df['amount_backs'] = df.apply(get_amount, axis=1)

    df = df.loc[:,['method', 'task', 'amount_backs']].set_index(['method', 'task'])
    df = df.sort_values(by=['method', 'task'], ascending=True)
    return df

def backs_textlen_ratio_user(uid):
    df = amount_backs_user(uid)
    df['text_len'] = textlen_user(uid)['text_len']
    df['ratio'] = df['amount_backs'] / df['text_len']
    return df

def backs_textlen_ratio_avg():
    df = backs_textlen_ratio_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += backs_textlen_ratio_user(uid)
    df['amount_backs'] = df['amount_backs'] / len(USER_IDS)
    df['text_len'] = df['text_len'] / len(USER_IDS)
    df['ratio'] = df['ratio'] / len(USER_IDS)
    return df


def backsequs_user_task(uid, tid):
    df = log_file(uid, tid)
    sequs = list()
    in_sequ = False
    c = 0
    for act in df['Action']:
        if in_sequ:
            if act == 'BACK':
                c += 1
            else:
                in_sequ = False
                sequs.append(c)
                c = 0
        else:  
            if act == 'BACK':
                in_sequ = True
                c = 1
            else:
                continue
    if in_sequ:
        sequs.append(c)
    return sequs

def amount_backs_user(uid):
    df = task_file(uid)

    def get_amount(row):
        return amount_backs_user_task(uid, row.name)
    df['amount_backs'] = df.apply(get_amount, axis=1)

    df = df.loc[:,['method', 'task', 'amount_backs']].set_index(['method', 'task'])
    df = df.sort_values(by=['method', 'task'], ascending=True)
    return df

def backsequs_user(uid):
    df = task_file(uid)

    def get_amount(row):
        return len(backsequs_user_task(uid, row.name))
    def get_avg_len(row):
        sequs = backsequs_user_task(uid, row.name)
        if len(sequs) == 0:
            return 0
        else:
            return sum(sequs)/len(sequs)
    df['amount_backsequs'] = df.apply(get_amount, axis=1)
    df['avg_len_backsequs'] = df.apply(get_avg_len, axis=1)

    df = df.loc[:,['method', 'task', 'amount_backsequs', 'avg_len_backsequs']].set_index(['method', 'task'])
    df = df.sort_values(by=['method', 'task'], ascending=True)
    return df

def backsequs_textlen_ratio_user(uid):
    df = backsequs_user(uid)
    df['text_len'] = textlen_user(uid)['text_len']
    df['ratio'] = df['amount_backsequs'] / df['text_len']
    return df

def backsequs_avg(info=True):
    if info:
        print('### Average Length of Backsequenses and ratio of sequences per character ###')
    df = backsequs_textlen_ratio_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += backsequs_textlen_ratio_user(uid)
    df['ratio'] = df['ratio'] / len(USER_IDS)
    df['avg_len_backsequs'] = df['avg_len_backsequs'] / len(USER_IDS)
    return df.loc[:, ['avg_len_backsequs', 'ratio']]


def amount_backs_boxplot(save=False, format='png'):
    boxplot_by_method(amount_backs_user, 'amount_backs', 
                        title='Number of Backspaces used', 
                        showfliers=False, 
                        save=save, 
                        filename='amount_backs',
                        format=format)

def backs_textlen_ratio_boxplot(save=False, format='png'):
    boxplot_by_method(backs_textlen_ratio_user, 'ratio', 
                        title='Ratio Number of Backspaces per character', 
                        showfliers=False, 
                        save=save, 
                        filename='backs_len_ratio',
                        format=format)

def amount_backsequs_boxplot(save=False, format='png'):
    boxplot_by_method(backsequs_user, 'amount_backsequs', 
                        title='Number of Backspace-Sequences performed', 
                        showfliers=False, 
                        save=save, 
                        filename='amout_backsequs',
                        format=format)

def amount_backsequs_textlen_ratio_boxplot(save=False, format='png'):
    boxplot_by_method(backsequs_textlen_ratio_user, 'ratio', 
                        title='Ratio Number of Backspace-Sequences per character', 
                        showfliers=False, 
                        save=save, 
                        filename='backseque_len_ratio',
                        format=format)

def backsequs_len_boxplot(save=False, format='png'):
    boxplot_by_method(backsequs_textlen_ratio_user, 'avg_len_backsequs', 
                        title='Length of Backspace-Sequences (in characters)', 
                        showfliers=False, 
                        save=save, 
                        filename='backseques_length',
                        format=format)


def backs_dataframe():
    data = []

    for uid in USER_IDS:
        for task in range(6):
            taskid = uid * 10 + task
            amount_backs = amount_backs_user_task(uid, taskid)
            back_sequs = backsequs_user_task(uid, taskid)
            amount_backsequs = len(back_sequs)
            avg_len_backsequs = sum(back_sequs)/amount_backsequs if amount_backsequs != 0 else 0
            data.append([taskid, amount_backs, amount_backsequs, avg_len_backsequs])

    df = pd.DataFrame(data, None, ["taskid", "amount_backs", "amount_backsequs", "avg_len_backsequs"])
    df.to_csv(DATA_DIR + '/backs.csv', index=False)

if __name__ == '__main__':
    # print(avg_by_method(backs_textlen_ratio_avg))
    # print(avg_by_method(backsequs_avg))
    # backs_textlen_ratio_boxplot(True)
    # amount_backsequs_textlen_ratio_boxplot(True)
    # backsequs_len_boxplot(True)
    amount_backsequs_boxplot(True, 'png')
    amount_backsequs_boxplot(True, 'svg')
    #backs_dataframe()