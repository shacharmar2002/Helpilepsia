"""
The server
"""

__author__ = "Shachar"

import threading
from flask import Flask, request

app = Flask(__name__)
FILE_LOCK = threading.Lock()


@app.route('/', methods=["POST"])
def get_input():
    """
    The main page
    :return: The string to send to the client
    """
    with FILE_LOCK:
        with open("output.txt", "a") as output_file:
            output_file.write(f"client number {request.form['client num']} send {request.form['input']}\n")
    return "0"
