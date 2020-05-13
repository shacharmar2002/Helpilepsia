import sqlite3

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    return conn

def login(conn, username, password):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Patients WHERE username = "{}" and password = "{}"'.format(username, password))
    rows = cur.fetchall()
    return rows

def sign_in(conn, username, password):
    sql = ''' INSERT INTO Patients( patientID, chipID, firstname, lastname, conatctID, username, password)
                 VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, username, password)
    conn.commit()


def get_events_by_user(conn, user_id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Events WHERE patientID = "{}"'.format(user_id))
    rows = cur.fetchall()
    return rows


def select_all_rows_by_table_name(conn, table_name):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM {}'.format(table_name))

    #cur.execute('select name from sqlite_master where type = "table"')
    rows = cur.fetchall()
    return(rows)


def insert_new_event(conn, *params):

    sql = ''' INSERT INTO Events(patientID, location, event_time, value, event_type)
              VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()

def close(conn):
    """ Commit changes and close connection to the database """
    # conn.commit()
    conn.close()


if __name__ == '__main__':


    sqlite_file = 'DBProject.db'
    table_name = 'Patients'
    params = (2, 212839682, 123.456,  123, 123, 123)
    conn, c = connect(sqlite_file)
    #total_rows(c, table_name)
    insert_new_event(conn, params)
    close(conn)