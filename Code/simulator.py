"""
Simulate multiple clients.
"""


__author__ = "Shahar"

import threading
# import socket
import time
import msvcrt
import requests
import traceback
import datetime
import DAL

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000
TEST_INFO = None
TEST_INFO_LOCK = threading.Lock()
RUNNING = True
RUNNING_LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()


def get_thread_input(thread_number):
    with TEST_INFO_LOCK:
        return TEST_INFO[thread_number]


def change_thread_input(thread_number):
    with TEST_INFO_LOCK:
        #print(TEST_INFO[thread_number])
        if TEST_INFO[thread_number] == b"0":
            TEST_INFO[thread_number] = b"1"
        elif TEST_INFO[thread_number] == b"1":
            TEST_INFO[thread_number] = b"2"
        elif TEST_INFO[thread_number] == b"2":
            TEST_INFO[thread_number] = b"0"



def get_running():
    with RUNNING_LOCK:
        return RUNNING


def set_running(value):
    global RUNNING
    with RUNNING_LOCK:
        RUNNING = value


def send_pulses(index):
    """
    Sends a "pulse" (number) through a socket until server closes.
    :param index: The index of the information to send.
    """
    path = str(DAL.__file__[:-7])
    conn = DAL.connect(path + r'\DBProject.db')
    patients = [item[0] for item in DAL.get_patient(conn)]

    while get_running():
        time.sleep(1)
        thread_input = get_thread_input(index)
        with PRINT_LOCK:
            print("Thread num:", index, ", input: ", thread_input)
        data = {}
        #TO DO-complete thread_input =1,2,3
        data["input"] = thread_input
        data["client_num"] = patients[index]
        data["position"] = "123"
        data["event_time"] = datetime.datetime.now()
        data["value"] = "123"



            #{"input": thread_input, "client num": index, "start_time": "123"}
        requests.post(
            f"http://{SERVER_IP}:{SERVER_PORT}/add_data", data)
        if (thread_input==b"2"):
            change_thread_input(index)


def start_threads(count):
    """
    Start all the threads.
    :param count: how many threads to start
    """
    for i in range(count):
        threading.Thread(target=send_pulses, args=(i,)).start()


def main():
    """
    Entry point of the simulator.
    """
    global TEST_INFO
    try:
        number_of_threads = int(input("How many threads?: "))
        TEST_INFO = [b"0" for _ in range(number_of_threads)]
        start_threads(number_of_threads)
        while get_running():
            key = msvcrt.getch().decode("ASCII")
            if key == 'q':
                set_running(False)
            elif key.isnumeric():
                change_thread_input(int(key))
    except Exception as e:
        set_running(False)
        traceback.print_tb(e)
    finally:
        input("Press enter to exit\n")


if __name__ == "__main__":
    main()
