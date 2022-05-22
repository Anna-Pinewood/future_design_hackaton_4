from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import random as rd
from prod_hours import run
from process import DataStorage
from advice import advice
from plot_main_page import get_data_main_plot
# from prediction_burnout import build_burnout_model

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app, resources={r"/*":{'origins':"*"}})
#CORS(app, resources={r"/*": {'origins': 'http://localhost:8080', 'allow_headers': 'Access-Control-Allow-Origin'}})

response_object = {
        'status': 'success'
}

date = None

#функция для чтения csv, файл в response_object['csv_file']
@app.route('/', methods=['GET', 'POST'])
def is_csv():
    if request.method == 'POST':
        file = request.files['file']
        rt = pd.read_csv(file)
        global date
        # model_burnout = build_burnout_model(date.notprod)
        # global model_burnout
        date = DataStorage(data=rt)
        response_object = {
        'status': 'success',
        'csv_file': rt.to_json()
        }
    return response_object


#useless
@app.route('/modeltype', methods=['GET', 'POST'])
def type():
    resp = {
        'status': 'success'
        }
    if request.method == 'POST':
        post_data = request.get_json()
        user_data['user_model'] = post_data['type']
        resp['type'] = post_data['type']
    return resp

user_data  = {
    'procrastination' : None,
    'work' : None,
    'workdaysleep' : None,
    'weekendsleep' : None
}

things = [
]

@app.route('/advice', methods=['GET'])
def advicing():
    global date
    print(date.data_schedule)
    res = advice(date)
    return res


@app.route('/user_form', methods=['GET', 'POST'])
def form():
    response = {
        'status': 'success',
    }
    if request.method == 'POST':
        post_data = request.get_json()
        user_data['procrastination'] = post_data.get('procrastination'),
        user_data['work'] = post_data.get('work'),
        user_data['workdaysleep'] = post_data.get('workdaysleep'),
        user_data['weekendsleep'] = post_data.get('weekendsleep'),
        user_data['ideal'] = post_data.get('ideal'),
        response['message'] = 'Data added!'

        global date
        date = DataStorage(answers=user_data)        
        print(user_data)
    elif request.method == 'GET':
        chart_data = []
        chart_data.append(([1, 2, 3, 4, 5, 6], [23, 46, 65, 76, 3, 4], 'chilling', rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] ), rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] )))
        chart_data.append(([23, 56, 345, 48, 93, 64], [53, 36, 46, 71, 23, 54], 'having fun', rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] ), rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] )))

        return  {'chart': chart_data }
    return jsonify(response)

#get route

@app.route('/things', methods=['GET', 'POST'])
def all_todos():
    reobject = {
        'status': 'success'
    }
    if request.method == 'POST':
        post_data = request.get_json()
        things.append({
            'name': post_data.get('name'),
            'time': post_data.get('time'),
            'done': post_data.get('done')})
        reobject['message'] = 'Todo added!'
    else:
        reobject['things'] = things
    return jsonify(reobject)


@app.route('/productive', methods=['GET'])
def prod():
#    data = arr[0]['csv_file']
    global date
    data = date.data_schedule
    answ = date.answers
    if data is not None:
        weekday, weekend = run(data=data)
    elif answ is not None:
        weekday, weekend = run(answers=answ)
    return {'data': [(weekday.X, weekday.Y, weekday.name, rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] ), rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']])), (weekend.X, weekend.Y, weekend.name, rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']] ), rd.choice([['#ecc7ff', '#ffb5ea', '#ff87b7', '#d6abff'], ['#ae9eff', '#eb7ad2', '#f02bcf', '#aa70e0'],['#b5e6ff', '#26ffdb', '#73b7ff', '#c599ff']]))  ]  }


@app.route('/chart', methods=['GET'])
def chart():
    print(date)
    if date is not None:
        res = get_data_main_plot(isprod=date.isprod,
                       nonprod=date.isprod,
                       isful=date.isful,
                       nonful=date.nonful,
                       sleep=date.sleep)
        print(res)
        return {'chart': res }
    else:
        return {'chart': 0 }


    

@app.route('/shark', methods=['GET'])
def shark():
    return("Shark 💌")


if __name__ == '__main__':
    app.run(debug=True)