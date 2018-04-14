import psycopg2
import psycopg2.extras
from config import config
 
conn = None
def connect():
    global conn
    """ Connect to the PostgreSQL database server """
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        return cur
     #    cur.execute('SELECT count(*) FROM game_info')
     #    count = cur.fetchone()
     #    print(count)
       
     # # close the communication with the PostgreSQL
     #    cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query_one(cur, qry):
    cur.execute(qry)
    data = cur.fetchone()
    return dict(data)

def query_mul(cur, qry):
    cur.execute(qry)
    data = cur.fetchall()
    dict_data = []
    for row in data:
        dict_data.append(dict(row))
    return dict_data
    
def disconnect(cur):
    if conn is not None:
        cur.close()
        conn.close()
        print('Database connection closed.')
    else:
        print('No connection exists')
