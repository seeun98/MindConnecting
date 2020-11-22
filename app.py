from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from mySchedule import getAllSchedules
client = MongoClient('localhost', 27017)
db = client.computerScience #'computerScience'라는 이름의 db 사용
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'



@app.route('/mySchedules_list')
def mySchedules_get():
    return render_template('mySchedule.html')

@app.route('/mySchedules_get/list', methods=['GET'])
def mySchedules_list():
    items = getAllSchedules()
    print(items)
    return jsonify({'result' : 'success', 'items' : items})


if __name__ == '__main__':
    app.run('0.0.0.0', port = 5050, debug = True)

