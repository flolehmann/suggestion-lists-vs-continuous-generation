import pandas as pd
from constants import INPUT_DIR, diverging_bar


def plot_table(tbl_name, save=False, format='png'):
    df = pd.read_csv(INPUT_DIR + '/' + tbl_name + '.csv',  index_col='Version', sep=';')

    title = df.index[0]
    df = df.drop(title)

    if title == 'no_title':
        title = ''

    diverging_bar(df, df.index, df.columns, title, save, tbl_name, format=format, folder='questionnaire')

def save_all_table_plots(format='svg'):
    # The combine and learning plots have to be edited with inkscape after generating
    for tbl in ['inspired', 'learning']:
        plot_table(tbl, True, format)

if __name__ == '__main__':
    save_all_table_plots('png')
    save_all_table_plots('svg')

