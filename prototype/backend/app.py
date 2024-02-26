from flask import Flask, request, json
from pyfiles.generator import Generator
from pyfiles.constants import SURVEY_LINK, AMOUNT_SUGGESTIONS
from pyfiles.model import Model

app = Flask(__name__)

g = Generator()
model = Model()

@app.route('/api/generate', methods=['POST'])
def generate_sentence():
    request_data = json.loads(request.data)
    sentence = request_data['content']

    while sentence[-1] == ' ':
        sentence = sentence[:-1]

    model.start_task_timer()

    index = len(sentence.split(' '))
    new_sen, t = g.generate_sentence(sentence)
    
    model.add_gen_time(t)

    return {'sentence': sentence,
            'new_sentence': new_sen,
            'index': index}


@app.route('/api/generate_options', methods=['POST'])
def generate_options():
    request_data = json.loads(request.data)
    pre = request_data['pre_sentence']
    new_opts = request_data['new_options']

    while pre[-1] == ' ':
        pre = pre[:-1]

    model.start_task_timer()
    model.task_logging(pre)

    sen, t = g.generate_multiple_options(pre, AMOUNT_SUGGESTIONS)
    
    model.add_gen_time(t)
    if(new_opts):
        model.increase_new_opts()

    return {
        'pre_sen': pre, 
        'sentences': sen
        }


@app.route('/api/user/<int:uid>') 
def set_user_id(uid):
    model.set_user_id(uid)
    return '', 204


@app.route('/api/questions')
def get_questions():
    return {'questions': model.get_questions()}


@app.route('/api/task/<int:id>') 
def get_task(id):
    model.set_current_task(id)
    return model.task_to_json()


@app.route('/api/task/<int:id>/start_timer') 
def start_timer(id):
    model.start_task_timer()
    return '', 204


@app.route('/api/task/<int:id>/end_timer') 
def end_timer(id):
    model.end_task_timer()
    return '', 204


@app.route('/api/task/store_result', methods=['POST']) 
def finished_task():
    request_data = json.loads(request.data)
    model.set_task_result(request_data['result'])
    return '', 204


@app.route('/api/task/log_input', methods=['POST'])
def log_input():
    request_data = json.loads(request.data)
    model.start_task_timer()
    model.task_logging(request_data['sentence'])
    return '', 204


@app.route('/api/task/<int:id>/rating', methods=['POST']) 
def set_rating(id):
    request_data = json.loads(request.data)
    model.set_task_rating(request_data['index'], request_data['rating'])
    return '', 204


@app.route('/api/task/<int:id>/store') 
def store_task(id):
    model.save_task(id)
    #model.set_no_curr_task()
    return '', 204


@app.route('/api/survey_link')
def get_survey_link():
    return {'link': SURVEY_LINK}


g.load_model()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
