"""
The server
"""

__author__ = "Shachar"

import threading
from flask import Flask, request, render_template
import Code.DAL

app = Flask(__name__)
FILE_LOCK = threading.Lock()


def string_by_code(parameters):
    input = parameters['input']
    str = f"client number {parameters['client_num']}" f" input {input} " f"position {parameters['position']} "
    str += f"start time {parameters['event_time']} " f"position {parameters['position']} "
    str += f"value {parameters['value']} \n"
    return str

@app.route('/')
def root():
    message = "Hello world"
    return render_template('index.html', rer=message, John= 'sag')

@app.route('/login', methods=['GET', 'POST'])
def login_root():
    if request.method == 'POST':
        conn = Code.DAL.connect('DBProject.db')
        rows = Code.DAL.login(conn, request.form['username'], request.form['password'])
        Code.DAL.close(conn)
        print(rows)
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/add_data', methods=["POST"])
def add_data():
    """
    The main page
    :return: The string to send to the client
    """
    with FILE_LOCK:
        with open("output.txt", "a") as output_file:
            output_file.write(string_by_code(request.form))
    input = request.form['input']
    client_num = request.form['client_num']
    position = request.form['position']
    conn = Code.DAL.connect('DBProject.db')
    event_time = request.form['event_time']
    value = request.form['value']
    Code.DAL.insert_new_event(conn, client_num, position, event_time, value, input)

    Code.DAL.close(conn)
    return "0"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")