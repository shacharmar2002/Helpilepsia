"""
The server
"""

__author__ = "Shachar"

import threading
from flask import Flask, request, render_template
import DAL

app = Flask(__name__)
FILE_LOCK = threading.Lock()


def string_by_code(parameters):
    input = parameters['input']
    str = f"client number {parameters['client_num']}" f" input {input} "
    if (input=='0'):
        str += f"start time {parameters['start_time']} " f"position {parameters['position']}"f"\n"
    elif(input=='1' or input=='2'):
        str += f"value {parameters['value']} " f"position {parameters['position']}"f"\n"
    elif(input=='3'):
        #To Do: send all of the array
        str+=f"history {parameters['history']}\n"
    return str

@app.route('/')
def root():
    message = "Hello world"
    return render_template('index.html', rer=message, John= 'sag')

@app.route('/add_data', methods=["POST"])
def add_data():
    """
    The main page
    :return: The string to send to the client
    """
    with FILE_LOCK:
        with open("output.txt", "a") as output_file:
            output_file.write(string_by_code(request.form))

    conn = DAL.connect('DBProject.db')
    DAL.insert_new_event(conn, request.form)
    DAL.close(conn)
    return "0"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")