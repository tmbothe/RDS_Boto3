from configparser import ConfigParser
import os
import psycopg2

DB_CONFIG_FILE = os.path.dirname(__file__)+'/database.ini'


def config(filename=DB_CONFIG_FILE, section='postgresql'):
    #create parser
    parser = ConfigParser()

    # read config
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception('section {0} not found in {1}',format(section,filename))
    return db



def connect_to_rds():
    conn = None
    try:
        params = config()
        print("Connecting to the Postgres database")

        conn = psycopg2.connect(**params)
        cur = conn.cursor() 

        #execute sql
        print('Postgres Sql Version')
        cur.execute('SELECT version()')

        #fetch the version
        db_version = cur.fetchone()
        print(f'The database Version is {db_version}')

        #close connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection close')

def create_tables():
    #provide sql commands

    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL
        ) 
        """,
        """
        CREATE TABLE accounts (
            account_id SERIAL PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL
        )
        """
    )

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)
        cur.close()

        conn.commit()
        print("Tables succesfully created.")
    except(Exception, psycopg2.DatabaseError) as  error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection close')

def insert_vendor_list(user_list):
    sql = "INSERT INTO users(user_name) VALUES (%s)"
    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql,user_list)
        conn.commit()
        cur.close()
    except(Exception , psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('All vendors inserted')
            print('Database connection close')

def get_users():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT user_id, user_name FROM users ORDER BY user_name")
        print("Numbers of users:", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_user(user_id, user_name):
    sql = """ UPDATE users
              SET user_name = %s 
              WHERE user_id = %s """

    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (user_name, user_id))

        updated_rows = cur.rowcount

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def delete_user(user_id):

    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

        rows_deleted = cur.rowcount

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted    




if  __name__=='__main__':
    connect_to_rds()
    create_tables()

    #insert_vendor_list([
    #     ('John Doe',),
    #     ('Douglas Smith',),
    #     ('Anthony Jenkins',),
    #     ('David Salazar',),
    #     ('Richard Forrester',),
    #     ('Shawn Reddick',),
    #     ('Philip Broyles',)
    # ])

    #get_users()

    #response = update_user(1, 'Niyazi')
    #print(response)
    #get_users()


    
   