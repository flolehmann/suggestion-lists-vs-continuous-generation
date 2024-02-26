from constants import USER_IDS, task_file, boxplot_by_method, avg_by_method


def textlen_user(uid, include_times=False, in_words=False):
    df = task_file(uid)

    def count_words(sen):
        l = sen.split(' ')
        while '' in l:
            l.remove('')
        return len(l)

    def count_characters(sen):
        return len(sen)

    if in_words:
        df['text_len'] = df['result'].apply(count_words)
    else:
        df['text_len'] = df['result'].apply(count_characters)

    cols = ['task', 'method', 'text_len']
    if include_times:
        cols.extend(['needed_time', 'time_generating'])

    df = df.loc[:,cols].set_index(['method', 'task'])
    df = df.sort_values(by=['method', 'task'], ascending=True)

    return df


def textlen_avg(info=True):
    if info:
        print('### Average text length (in characters) ###')
    df = textlen_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += textlen_user(uid)
    df['text_len'] = df['text_len'] / len(USER_IDS)
    return df


def wpm_user(uid, actual_words=False):

    df = textlen_user(uid, True, actual_words)

    if actual_words:
        df['wpm'] = (df['text_len'] / (df['needed_time'] - df['time_generating'])) * 60
    else:
        df['wpm'] = (df['text_len'] / 5) / ((df['needed_time'] - df['time_generating']) / 60)

    return df.loc[:, ['wpm']]


def taskcompletion_user(uid):

    df = textlen_user(uid, True)
    df['task_completiontime'] = df['needed_time'] - df['time_generating']

    return df.loc[:, ['task_completiontime']]


def wpm_avg(info=True):
    if info:
        print('### Average Words per minute ###')
    df = wpm_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += wpm_user(uid)
    df['wpm'] = df['wpm'] / len(USER_IDS)
    return df


def wpm_avg_by_method():
    df = wpm_avg()
    df = df.groupby(level='method').sum()
    df = df/2
    return df

def wpm_boxplot(save=False, format='png'):
    boxplot_by_method(wpm_user, 'wpm', 
                        title='Words per Minute',
                        showfliers=False,
                        save=save,
                        filename='wpm',
                        format=format)

def textlen_boxplot(save=False, format='png'):
    boxplot_by_method(textlen_user, 'text_len', 
                        title='Text Length (in characters)',
                        showfliers=False,
                        save=save, 
                        filename='textlen',
                        format=format)

def tasktime_boxplot(save=False):
    boxplot_by_method(taskcompletion_user, 'task_completiontime',
                        title='7)  Task completion time',
                        showfliers=False,
                        save=save,
                        filename='taskcompletiontime')

if __name__ == '__main__':  
    #print(avg_by_method(wpm_avg))
    #print(avg_by_method(textlen_avg))
    wpm_boxplot(True)
    #textlen_boxplot(True)
    #print(wpm_user(14))
    
