import psycopg2
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
        cur = conn.cursor()
        
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

def query(cur, qry):
    cur.execute(qry)
    return cur.fetchone()
    
def disconnect(cur):
    if conn is not None:
        cur.close()
        conn.close()
        print('Database connection closed.')
    else:
        print('No connection exists')
