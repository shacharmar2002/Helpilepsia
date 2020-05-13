"""
The server
"""

__author__ = "Shachar"

import threading
from flask import Flask, request, render_template, session
import DAL


app = Flask(__name__)
app.secret_key = "any random string"
FILE_LOCK = threading.Lock()


def string_by_code(parameters):
    input = parameters['input']
    str = f"client number {parameters['client_num']}" f" input {input} " f"position {parameters['position']} "
    str += f"start time {parameters['event_time']} " f"position {parameters['position']} "
    str += f"value {parameters['value']} \n"
    return str

@app.route('/')
def root():
    return get_main_page()

@app.route('/logout')
def logout():
    session["patientID"] = None
    session["chipID"] = None
    session["firstname"] = None
    session["lastname"] = None
    session["medical_state"] = None
    session["location"] = None
    session["contactID"] = None
    session["username"] = None
    session["password"] = None

    return get_main_page()

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        conn = DAL.connect('DBProject.db')
        DAL.sign_in(conn, request.form['username'], request.form['password'])
        DAL.close(conn)
        session["patientID"] = None
        session["chipID"] = None
        session["firstname"] = None
        session["lastname"] = None
        session["contactID"] = None
        session["username"] = request.form['username']
        session["password"] = request.form['password']
        return get_main_page()
    elif request.method == 'GET':
        return render_template("sign_in.html")

@app.route('/login', methods=['GET', 'POST'])
def login_root():
    if request.method == 'POST':
        conn = DAL.connect('DBProject.db')
        rows = DAL.login(conn, request.form['username'], request.form['password'])
        DAL.close(conn)
        if (len(rows) == 0):
            return render_template('login.html', error = "username or password is invalid")
        session["patientID"], session["chipID"], session["firstname"], session[
            "lastname"], session["medical_state"], session["location"],\
        session["contactID"], session["username"], session["password"] = rows[0]
        return get_main_page()
    elif request.method == 'GET':
        return render_template('login.html', error = "")

def get_main_page():
    events = []
    if (session["patientID"] != None):
        events = get_events(session["patientID"])
    return render_template('index.html', events = events)
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
    conn = DAL.connect('DBProject.db')
    event_time = request.form['event_time']
    value = request.form['value']
    DAL.insert_new_event(conn, client_num, position, event_time, value, input)

    DAL.close(conn)
    return "0"
def get_events(user_id):
    conn = DAL.connect('DBProject.db')
    rows = DAL.get_events_by_user(conn, user_id)
    DAL.close(conn)
    return rows
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")