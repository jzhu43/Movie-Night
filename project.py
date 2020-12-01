# # Python file for database Final Phase of Project
# # Created by Malia Bowman and Jason Zhu

import os
import sqlite3
from sqlite3 import Error
   ## Include SQLite package
import random

################ Connect SQLite Database ################

# db_connection = None # Define the connection parameter
# #db_name = "/Users/bowma/CSE 111/Project/CSE111-Project-F20/moviesdata.db" # Specify the full path of Database file
# db_name = "/Users/bowma/CSE 111/Project/CSE111-Project-F20/project.db"
# #db_name = "moviesdata.db"


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")
def search(_conn):
    print("\nLet's search for your movie!") 
    # movie = raw_input("\nWhat movie do you want to search for? The system will give you information about the movie. Enter the name: ")
    # print(movie)
    try:
        movie = raw_input("\nWhat movie do you want to search for? The system will give you information about the movie. Enter the name: ")
        sql = """SELECT m_title, m_year, m_length, m_director, m_company
                FROM movies
                WHERE m_title = ?"""
        cur = _conn.cursor()
        cur.execute(sql, (movie,))
        rows = cur.fetchall()
        
        if len(rows) == 0:
            print("The movie does not exist in the Movie Night system :(")
            exit()
        else:
            l = ("Title | Year | Length | Director | Company of Movie")
            print(l)
            for row in rows:
                # l = (row[0], row[1], row[2], row[3], row[4])
                # print(l)
                # print('|'.join([str(r) for r in row]) + "\n")
                print('|'.join([str(r) for r in row]))
        year = raw_input("\nEnter the year of the movie you searched for to know more information about the film:")
        if len(year) == 0:
            exit() #This takes a bit of time to exit (for some reason)
        sql = """SELECT a_name, a_dob
                FROM actor, movies, appears
                WHERE a_actorid = app_actorid
                    AND m_movieid = app_movieid
                    AND m_title = ?
                    AND m_year = ?"""
        cur = _conn.cursor()
        cur.execute(sql, (movie, year,))
        rows = cur.fetchall()
        l = ("Actor Name | Date of Birth:")
        print(l)
        for row in rows:
                print('|'.join([str(r) for r in row]))

        sql = """SELECT r_imdb, r_rottent
                FROM review, movies
                WHERE r_movieid = m_movieid
                    AND m_title = ?
                    AND m_year = ?"""
        cur = _conn.cursor()
        cur.execute(sql, (movie, year,))
        rows = cur.fetchall()
        l = ("\nIMDB review | Rotten Tomato review:")
        print(l)
        for row in rows:
                print('|'.join([str(r) for r in row]) + "\n")

        sql = """SELECT g_genre
                FROM genre, movies
                WHERE g_movieid = m_movieid
                    AND m_title = ?
                    AND m_year = ?"""
        cur = _conn.cursor()
        cur.execute(sql, (movie, year,))
        rows = cur.fetchall()
        l = ("Genre: ")
        print(l)
        for row in rows:
                print('|'.join([str(r) for r in row]) + "\n")

    except Error as e:        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")     
    

def recommend(_conn):
    int

def modify(_conn):
    int

def main():
   database = r"moviesdata.db"

   # create a database connection
   conn = openConnection(database)
   
   print("\nHello, welcome to Movie Night! What would you like to do?")
   print("\n1. Search for a movie")
   print("\n2. Receive a recommendation based on your interests")
   print("\n3. Modify the movie system's information")
   print("\nEnter the number of what you would like to do: ")

   answer = input()
   with conn:
    if answer == 1:
        search(conn)
    if answer == 2:
        recommend(conn)
    if answer ==3:
        modify(conn)

   closeConnection(conn, database)


if __name__ == '__main__':
    main()