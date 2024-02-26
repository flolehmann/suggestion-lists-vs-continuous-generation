from constants import DATA_DIR, USER_IDS, task_file, log_file, boxplot_by_method, avg_by_method
from wpm import textlen_avg, textlen_user
import pandas as pd


def amount_actions_user_task(uid, tid, method=-1, amount_new_opts=-1):
    df = log_file(uid, tid)
    df = df.dropna(axis=0)

    if method == -1:
        method = task_file(uid).loc[tid, 'method']

    if method == 0 or method == 1:
        return len(df)

    elif method == 2:
        if amount_new_opts == -1:
            amount_new_opts = task_file(uid).loc[tid, 'amount_new_opts']
        return len(df) + amount_new_opts

    else:
        return None


def amount_actions_user(uid):
    df = task_file(uid)

    def get_amount(row):
        return amount_actions_user_task(uid, row.name, row['method'], row['amount_new_opts'])
    
    df['amount_actions'] = df.apply(get_amount, axis=1)
    
    df = df.loc[:,['method', 'task', 'amount_actions']].set_index(['method', 'task'])
    df = df.sort_values(by=['method', 'task'], ascending=True)

    return df

def actions_length_ratio_user(uid):
    df = amount_actions_user(uid)
    df2 = textlen_user(uid)

    df['text_len'] = df2['text_len']
    df['ratio'] = df['amount_actions'] / df['text_len']

    return df


def amount_actions_avg(info=True):
    if info:
        print('### Average Actions performed ###')
    df = amount_actions_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += amount_actions_user(uid)
    df['amount_actions'] = df['amount_actions'] / len(USER_IDS)
    return df

def amount_actions_to_length_ratio(info=True):
    if info:
        print('### Average amount of Actions performed for one character ###')
    df = amount_actions_avg(False)
    df['text_len'] = textlen_avg(False)['text_len']
    df['ratio'] = df['amount_actions'] / df['text_len']

    return df


def amount_actions_boxplot(save=False, format='png'):
    boxplot_by_method(amount_actions_user, 'amount_actions', 
                    title='Number of Actions performed', 
                    showfliers=False, 
                    save=save, 
                    filename='amount_actions',
                    format=format)

def actions_length_ratio_boxplot(save=False, format='png'):
    boxplot_by_method(actions_length_ratio_user, 'ratio', 
                        title='Ratio Number of Actions per character', 
                        showfliers=False, 
                        save=save, 
                        filename='act_len_ratio',
                        format=format)

def actions_dataframe():
    data = []

    for uid in USER_IDS:
        for task in range(6):
            taskid = uid * 10 + task
            amount_actions = amount_actions_user_task(uid, taskid)
            data.append([taskid, amount_actions])

    df = pd.DataFrame(data, None, ["taskid", "amount_actions"])
    df.to_csv(DATA_DIR + '/actions.csv', index=False)

if __name__ == '__main__':
    #print(avg_by_method(amount_actions_to_length_ratio))
    #actions_length_ratio_boxplot(True)
    #actions_dataframe()
    amount_actions_boxplot(True, 'png')
