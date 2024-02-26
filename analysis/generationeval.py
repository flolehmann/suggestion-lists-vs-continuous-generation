from constants import USER_IDS, task_file, log_file
from wpm import textlen_avg


def generations_user(uid):
    df = task_file(uid)

    df = df.loc[:, ['task', 'method', 'amount_generations']].set_index(['method', 'task'])
    df = df.drop(index = (0,0))
    df = df.drop(index = (0,1))
    df = df.sort_values(by=['method', 'task'], ascending=True)

    return df


def generations_avg():
    df = generations_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += generations_user(uid)
    df['amount_generations'] = df['amount_generations'] / len(USER_IDS)

    return df


def new_options_user(uid):
    df = task_file(uid)
    
    df = df.loc[:, ['task', 'method', 'amount_new_opts']].set_index(['method', 'task'])
    for t in range(2):
        for m in range(2):
            df.drop(index=(m, t), inplace=True)
    df = df.sort_values(by=['method', 'task'], ascending=True)

    return df


def new_options_avg():
    df = new_options_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += new_options_user(uid)
    df['amount_new_opts'] = df['amount_new_opts'] / len(USER_IDS)

    return df


def amount_chosen_options_user_task(uid, tid):
    df = log_file(uid, tid) 
    df = df.dropna()

    def got_chosen(act):
        if len(act) <= 1:
            return False
        elif act != 'SPACE' and act != 'BACK' and act != '\\n':
            return True
        else:
            return False

    df = df[df['Action'].apply(got_chosen)]

    return len(df)


def amount_chosen_options_user(uid):
    df = task_file(uid)

    def get_amount_chosen(row):
        return amount_chosen_options_user_task(uid, row.name)

    df['amount_chosen_opts'] = df.apply(get_amount_chosen, axis=1)

    df = df.loc[:, ['task', 'method', 'amount_generations', 'amount_new_opts', 'amount_chosen_opts']].set_index(['method', 'task'])
    for t in range(2):
        for m in range(2):
            df.drop(index=(m, t), inplace=True)
    df = df.sort_values(by=['method', 'task'], ascending=True)

    return df


def amount_chosen_options_avg(info=True):
    if info:
        print('### Average amount of Options generated, refreshed and used ###')
    df = amount_chosen_options_user(USER_IDS[0])
    for uid in USER_IDS[1:]:
        df += amount_chosen_options_user(uid)
    df['amount_generations'] = df['amount_generations'] / len(USER_IDS)
    df['amount_new_opts'] = df['amount_new_opts'] / len(USER_IDS)
    df['amount_chosen_opts'] = df['amount_chosen_opts'] / len(USER_IDS)

    return df


def amount_chosen_options_to_length_ratio(info=True):
    if info:
        print('### Average amount of Options used for one word ###')
    df = amount_chosen_options_avg(False)
    df['text_len'] = textlen_avg(False)['text_len']
    df['ratio'] = df['amount_chosen_opts'] / df['text_len']

    return df.loc[:, ['amount_chosen_opts', 'text_len', 'ratio']]


if __name__ == '__main__':      
    print(generations_avg())
    print(amount_chosen_options_to_length_ratio())