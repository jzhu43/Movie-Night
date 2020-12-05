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
            main()
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
        if len(rows) != 0:
            l = ("Genre: ")
            print(l)
            for row in rows:
                    print('|'.join([str(r) for r in row]) + "\n")

        print("Would you like to search again (Enter 1) -or- receive a recommendation (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 0)?:")
        answer = input()
        if answer == 0:
            exit()    
        if answer == 1:
            # print("YES")
            search(_conn)
        if answer == 2:
            # print("YES")
            recommend(_conn)
        if answer == 3:
            # print("YES")
            modify(_conn)
        
    except Error as e:        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")     
    

def recommend(_conn):
    #############################################################################
    # when we demo:
    #   actor: James Dean
    #   genre: DRAMA
    #############################################################################

    try:
        print("To receive better recommendation results, provide the following information:")
        print("Note: Based on your inputs, we will generate different recommendations. Please, be patient as this might take some time! :)")

        director = raw_input("The director: ")
        actor = raw_input("The actor: ")
        role = raw_input("The role of the actor: ")
        year = raw_input("The year: ")
        length = raw_input("The length of the movie: ")
        genre = raw_input("The genre of the movie: ")
        genre_2 = raw_input("Another genre of the movie: ")
        review = raw_input("The review score (1-10) of the movie: ")
        production = raw_input("The production of the movie: ")
        company = raw_input("The company of the movie: ")
       
        # if len(director) == 0:
        #     print("Empty")
        # if len(actor) == 0:
        #     print("Empty")
        # if len(role) == 0:
        #     print("Empty")
        # if len(year) == 0:
        #     print("Empty")
        # if len(length) == 0:
        #     print("Empty")
        # if len(genre) == 0:
        #     print("Empty")
        # if len(review) == 0:
        #     print("Empty")
        # if len(production) == 0:
        #     print("Empty")
        # if len(company) == 0:
        #     print("Empty")
        
        l = ("\nTitle | Year | Genre:")
        sql = """SELECT m_title, m_year, g_genre
                FROM movies, genre
                WHERE m_movieid = g_movieid
                    AND g_genre LIKE ?
                ORDER BY m_title ASC;"""
        cur = _conn.cursor()
        cur.execute(sql, (genre,))
        rows = cur.fetchall()
        if len(genre) != 0:
            print(l)
            for row in rows:
                    l = (row[0], row[1], row[2])
                    print(l)
        l = ("\nTitle | Year | Actor | Actor Date of Birth:")
        sql = """SELECT m_title, m_year, a_name, a_dob
                FROM actor, movies, appears
                WHERE m_movieid = app_movieid
                AND a_actorid = app_actorid
                AND a_name LIKE ? """
        cur = _conn.cursor()
        cur.execute(sql, (actor,))
        rows = cur.fetchall()
        if len(actor) != 0:
            print(l)
            for row in rows:
                    l = (row[0], row[1], row[2], row[3])
                    print(l)

        if len(actor) != 0 and len(genre) != 0:
            l = ("\nTitle | Year | Genre | Actor | Actor Date of Birth:")
            sql = """SELECT m_title, m_year, g_genre, a_name, a_dob
                    FROM actor, movies, appears, genre
                    WHERE m_movieid = app_movieid
                    AND a_actorid = app_actorid
                    AND m_movieid = g_movieid
                    AND a_name LIKE ? 
                    AND g_genre LIKE ?
                ORDER BY m_title ASC;"""
            cur = _conn.cursor()
            cur.execute(sql, (actor, genre,))
            rows = cur.fetchall()
            if len(rows) != 0: ####### if there are any tuples that have the actor and the genre we inputed, it will print the info
                print(l)
                for row in rows:
                            l = (row[0], row[1], row[2], row[3], row[4])
                            print(l)
            
        print("\nWould you like to search (Enter 1) -or- receive a recommendation again (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 0)?:")
        answer = input()
        if answer == 0:
            exit()    
        if answer == 1:
            # print("YES")
            search(_conn)
        if answer == 2:
            # print("YES")
            recommend(_conn)
        if answer == 3:
            # print("YES")
            modify(_conn)
        
    except Error as e:        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")   

def modify(_conn):
    try:
        # print("IN modify function")
        print("Would you like to search (Enter 1) -or- receive a recommendation again (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 0)?:")
        answer = input()
        if answer == 0:
            exit()    
        if answer == 1:
            # print("YES")
            search(_conn)
        if answer == 2:
            # print("YES")
            recommend(_conn)
        if answer == 3:
            # print("YES")
            modify(_conn)
    except Error as e:        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")

def main():
    database = r"moviesdata.db"

    # create a database connection
    conn = openConnection(database)

    print("Hello, welcome to Movie Night! What would you like to do?")
    print("1. Search for a movie")
    print("2. Receive a recommendation based on your interests")
    print("3. Modify the movie system's information")
    print("4. Leave Movie Night")
    print("Enter the number of what you would like to do: ")

    answer = input()
    # try:
    #    ans = int(answer)
    # except ValueError:
    #     print("Input is not a number.")
    #     main()

    with conn:
        if answer == 1:
            search(conn)
        if answer == 2:
            recommend(conn)
        if answer == 3:
            modify(conn)
        if answer == 4:
            exit()

    closeConnection(conn, database)


if __name__ == '__main__':
    main()