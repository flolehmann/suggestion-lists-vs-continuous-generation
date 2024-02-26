import os
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# All ids of users for which data is stored
USER_IDS = list(range(12, 33))
USER_IDS.remove(29) # There was no user with the id 21

# There are two uses which shouldn't included when evaluating logging data,
# but can be used when evaluating question data
EVALUATE_LOG_DATA = True
if EVALUATE_LOG_DATA:
    USER_IDS.remove(13) # User 13 had bugs on one technique
    USER_IDS.remove(30) # User 30 done it on laptop

# Directory where the data to evaluate get stored
DATA_DIR = os.getcwd() + '/data'

# Directory for the output of the plots
OUTPUT_DIR = os.getcwd() + '/plots'

# Directory for the input of the tables to plot from
INPUT_DIR = os.getcwd() + '/tables'

# Gets the task file based on the userId
def task_file(uid):
    return pd.read_csv(DATA_DIR +'/user' + str(uid) + '/' + str(uid)  +'-tasks.csv', index_col='taskid', sep=';')

# Gets the log file based on the userId and the taskId
def log_file(uid, tid):
    if tid < 6:
        tid = uid*10 + tid
    return pd.read_csv(DATA_DIR +'/user' + str(uid) + '/' + str(uid)  + '-logs/task' + str(tid) + '.csv', sep=';')


# The questions after each task
QUESTIONS = [
    'I am satisfied with the text.',
    'It was easy for me to write the text.',
    'I feel like I am the author of the text.',
    'The interaction method was suitable for this task.',
    'The interaction method helped me writing the text.',
    'The interaction method influenced the wording of the text.'
]

def avg_by_method(func):
    """
    Funciton to average a dataframe by the used method. Instead of that the dataframe is given directly, a function is given which creates the dataframe.

    Args:
        func (function): Function which provides the dataframe to average. Takes no parameters an returns a pandas DataFrame

    Returns:
        pd.DataFrame: Dataframe which got averaged by the mehtod.
    """
    df = func()
    df = df.groupby(level='method').sum()
    df = df/2
    return df

def diverging_bar(df, idxs, names, title='', save=False, filename='', format='svg', folder='', num_par=18):
    """ 
    Function to create a diverging bar char based on a given dataframe.
    This is used for displaying the results of the likert questions.

    Args:
        df (pd.DataFrame): Dataframe which should be represented as a diverging bar char. The dataframe has to have five columns. 
        idxs (list): Indexes which should stand on the x-axis of the diagramm.
        names (list): Names of the different bar parts ranging over the y-axis.
        title (str, optional): Title of the chart. Defaults to ''.
        save (bool, optional): Indicates wether the chart should be saved as a file or just shown. Defaults to False.
        filename (str, optional): Name of the file, if the chart should be saved. Defaults to ''.
        format (str, optional): Format of the image, if the chart should be saved. Defaults to 'svg'.
        folder (str, optional): ...
        num_par (int, optional): Number of participants that took part. Defaults to 18.
    """
    diverging = go.Figure()

    n1 = -1*df.iloc[:, 2] / 2
    n2 = n1 - df.iloc[:, 1]
    n3 = n2 - df.iloc[:, 0]
    p1 = -1* n1
    p2 = p1 + df.iloc[:, 3]

    b1 = -num_par
    x1 = num_par+n3
    b2 = p2 + df.iloc[:, 4]
    x2 = num_par-b2

    positions = [n3, n2, n1, p1, p2]

    colors = ['firebrick','lightcoral','darkgrey','cornflowerblue', 'darkblue']

    diverging.add_trace(go.Bar( x=x1,
                                y=idxs,
                                base=b1,
                                orientation='h',
                                marker={'color': 'rgba(0,0,0,0)',
                                'line':{'width':0}},
                                showlegend=False ))

    for i, col in enumerate(df.columns):
        diverging.add_trace(go.Bar( x=df[col],
                                    y=idxs,
                                    base=positions[i],
                                    orientation='h',
                                    name=names[i],
                                    marker={'color': colors[i]} ))

    diverging.add_trace(go.Bar( x=x2,
                                y=idxs,
                                base=b2,
                                orientation='h',
                                marker={'color': 'rgba(0,0,0,0)',
                                'line':{'width':0}},
                                showlegend=False ))
    
    # Specifying the layout of the plot
    diverging.update_layout(barmode='relative',
                            height=400,
                            width=700,
                            yaxis_autorange='reversed',
                            bargap=0.5,
                            legend_orientation='v',
                            legend_x=1.1, legend_y=0,
                            title=title,
                            titlefont={'color': 'black', 'size':16},
                            font={'color': 'black', 'size':13},
                            plot_bgcolor ='white',
                            xaxis=dict(
                                tickmode = 'array',
                                tickvals = [-20, -15, -10, -5, 0, 5, 10, 15, 20],
                                ticktext = [20, 15, 10, 5, 0, 5, 10, 15, 20])
                            )
    diverging.update_xaxes(gridcolor='lightgrey', gridwidth=1, zerolinewidth=2, zerolinecolor='black', showline=True, mirror=True, linecolor='black')
    diverging.update_yaxes(showline=True, mirror=True, linecolor='black')

    if save:
        out = OUTPUT_DIR
        if folder != '':
            out += '/' + folder
            if not os.path.exists(out):
                os.mkdir(out)
        out += '/' + format
        if not os.path.exists(out):
            os.mkdir(out)
        diverging.write_image(out + '/' + filename + '.' + format)
    else:
        diverging.show()


def boxplot_by_method(func, col_name, title='', showfliers=False,  save=False, filename='', format='svg'):
    """
    Function to create a boxplot, where the values are sorted by the used method.
    This is used for displaying the results of the logging.

    Args:
        func (function): Function that gets called for every user-id to get a dataframe from which you bild the boxplot. Function should take an int and return a pandas DataFrame.
        col_name (str): Name of the column which should be used for the boxplot.
        title (str, optional): Title of the chart. Defaults to ''.
        showfliers (bool, optional): Indicator if fliers should be shown in the boxplot or not. Defaults to False.
        save (bool, optional): Indicates wether the chart should be saved as a file or just shown. Defaults to False.
        filename (str, optional): Name of the file, if the chart should be saved. Defaults to ''.
        format (str, optional): Format of the image, if the chart should be saved. Defaults to 'svg'.
    """
    df = pd.DataFrame(columns=['V0', 'V1', 'V2'])

    for uid in USER_IDS:
        tmp = func(uid)
        for t in range(2):
            v = {'V0':0, 'V1':0, 'V2':0}
            for m in range(3):
                k = 'V' + str(m)
                v[k] = tmp.loc[(m, t), col_name]
            df = df.append(v, ignore_index=True)

    plt.rcParams.update({'font.size': 13})

    fig, ax = plt.subplots()
    bp = ax.boxplot(df, 
                    patch_artist=True,  # fill with color
                    labels=['Std. Input', 'Cont. Gen. Text', 'Writ. with Sugg.'],  # will be used to label x-ticks
                    showfliers=showfliers)

    colors = ['pink', 'lightblue', 'lightgreen']

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)  

    for patch in bp['medians']:
        patch.set_linewidth(1.3) 

    ax.set_title(title)

    if save:
        out = OUTPUT_DIR + '/logging/' + format
        if not os.path.exists(out):
            os.mkdir(out)
        plt.savefig(out + '/' + filename + '.' + format)
    else:
        plt.show()
