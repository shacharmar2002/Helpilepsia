import sqlite3

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c


def total_rows(cursor, table_name):
    """ Returns the total number of rows in the database """
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]


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


    for row in rows:
        print(row)


def insert_new_event(conn, params):

    sql = ''' INSERT INTO Events(eventID, patientID, location, event_start_time, event_duration, value)
              VALUES(?, ?, ?, ?, ?, ?) '''

    cur = conn.cursor()
    cur.execute(sql, params)
    print(cur.lastrowid)
    return cur.lastrowid

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