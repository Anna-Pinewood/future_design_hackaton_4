from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
#CORS(app, resources={r"/*": {'origins': 'http://localhost:8080', 'allow_headers': 'Access-Control-Allow-Origin'}})


@app.route('/', methods=['GET', 'POST'])
def is_csv():
    response_object = {
        'status': 'success'
    }
    if request.method == 'POST':
        file = request.files['file']
        rt = pd.read_csv(file)
        response_object = {
        'status': 'success',
        'csv_file': rt.to_json()
        }
    return response_object


@app.route('/modeltype', methods=['GET', 'POST'])
def type():
    resp = {
        'status': 'success'
        }
    if request.method == 'POST':
        post_data = request.get_json()
        user_data['user_model'] = post_data['type']
        print(user_data['user_model'])
        resp['type'] = post_data['type']
    return resp

user_data  = {
    'user_model': None
}

things = [
    {   'name': 'sleep',
        'time': '23:00-8:00',
        'done': True
    },
    {   'name': 'eat',
        'time': '8:00-9:00',
        'done': False
    },
    {   'name': 'idk',
        'time': '8:00-9:00',
        'done': True
    }
]

#get route

@app.route('/things', methods=['GET', 'POST'])
def all_todos():
    response_object = {
        'status': 'success'
    }
    if request.method == 'POST':
        post_data = request.get_json()
        things.append({
            'name': post_data.get('name'),
            'time': post_data.get('time'),
            'done': post_data.get('done')})
        response_object['message'] = 'Todo added!'
    else:
        response_object['things'] = things
    return jsonify(response_object)



@app.route('/shark', methods=['GET'])
def shark():
    return("Shark 💌")


if __name__ == '__main__':
    app.run(debug=True)