#Jake Varley
#from terminal to access postgres:
#sudo -u postgres psql nlptweets
#nlptweets=# select created_at from tweets;
import psycopg2
import numpy as np
import matplotlib.pyplot as plt

def get_connection():
    conn = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
    return conn

def grab_all_times():
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("SELECT created_at from tweets;")
    result = cur.fetchall()
    return result
