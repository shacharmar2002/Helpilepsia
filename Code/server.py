"""
The server
"""

__author__ = "Shaachar"

import threading
from flask import Flask, request, render_template, session
import DAL
import hash_code
import send_email

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


@app.route('/contact_sign_in', methods=['GET', 'POST'])
def contact_sign_in():
    if request.method == 'POST':
        conn = DAL.connect('DBProject.db')
        try:
            DAL.contact_sign_in(conn, request.form['contactID'],
                                request.form['firstname'],
                                request.form['lastname'],
                                request.form['phone'],
                                session['patientID'],
                                request.form['email'])
        finally:
            DAL.close(conn)

        session["contactID"] = request.form['contactID']
        session["contact_firstname"] = request.form['firstname']
        session["contact_lastname"] = request.form['lastname']
        session["phone"] = request.form['phone']
        session["email"] = request.form['email']
        return get_main_page()
    elif request.method == 'GET':
        return render_template("contact_sign_in.html")


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        conn = DAL.connect('DBProject.db')
        hash, salt = hash_code.hash_password(request.form['password'])
        try:
            DAL.sign_in(conn, request.form['patientID'],
                        request.form['chipID'],
                        request.form['firstname'], request.form['lastname'],
                        request.form['contactID'], request.form['username'],
                        hash, salt)
        finally:
            DAL.close(conn)
        DAL.close(conn)
        session["patientID"] = request.form['patientID']
        session["chipID"] = request.form['chipID']
        session["firstname"] = request.form['firstname']
        session["lastname"] = request.form['lastname']
        session["contactID"] = request.form['contactID']
        session["username"] = request.form['username']
        session["password"] = hash
        session["salt"] = salt
        return render_template("contact_sign_in.html")
    elif request.method == 'GET':
        return render_template("sign_in.html")


@app.route('/login', methods=['GET', 'POST'])
def login_root():
    rows = []
    if request.method == 'POST':
        conn = DAL.connect('DBProject.db')
        rows = DAL.login(conn, request.form['username'])
        if (len(rows) == 0):
            return render_template('login.html',
                                   error="username is invalid")
        patientID, chipID, firstname, lastname, medical_state, location, contactID, username, password, salt = \
            rows[0]
        if_true = hash_code.verify_password(password,
                                            salt,
                                            request.form['password'])
        DAL.close(conn)
        if (not if_true):
            return render_template('login.html',
                                   error="password is invalid")
        session["patientID"] = patientID
        session["chipID"] = chipID
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["contactID"] = contactID
        session["username"] = username
        session["password"] = str(hash)
        session["salt"] = str(salt)
        return get_main_page()
    elif request.method == 'GET':
        return render_template('login.html', error="")


def get_main_page():
    events = []
    columns = []
    if ("patientID" in session):
        events, columns = get_events(session["patientID"])
    return render_template('index.html', events=events, columns=columns)


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

    if (input == "1"):
        rows = DAL.GET_contact_by_id(conn, client_num)
        if (len(rows) != 0):
            contactID, contact_firstname, contact_lastname, phone, patientID, email = \
                rows[0]
            send_email.send_email(email,
                                  "hello " + contact_firstname + " your relative is having an epileptic seizure in this landmarks please send him help:" + position)
    DAL.close(conn)
    return "0"


def get_events(user_id):
    conn = DAL.connect('DBProject.db')
    rows, columms = DAL.get_events_by_user(conn, user_id)
    DAL.close(conn)
    return rows, columms


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
