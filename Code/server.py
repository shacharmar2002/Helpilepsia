"""
The server
"""

__author__ = "Shachar"

import threading
from flask import Flask, request, render_template

app = Flask(__name__)
FILE_LOCK = threading.Lock()


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
            output_file.write(f"client number {request.form['client num']}"
                              f" send {request.form['input']}\n")
    return "0"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
