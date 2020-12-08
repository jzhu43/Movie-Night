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
    #print("++++++++++++++++++++++++++++++++++")
    #print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        #print("success")
    except Error as e:
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

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
####### SEARCH FUNCTION ######################################################################################################################################
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

        print("Would you like to search again (Enter 1) -or- receive a recommendation (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 4)?:")
        answer = input()
        if answer == 4:
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
####### RECOMMEND FUNCTION ######################################################################################################################################
def recommend(_conn):
    #############################################################################
    # when we demo:
    #   actor: James Dean
    #   genre: DRAMA
    #   genre_2: ACTION
    #   year: 2005
    #   director: D.W. Griffith
    #############################################################################

    try:
        print("To receive better recommendation results, provide the following information:")
        print("Note: Based on your inputs, we will generate different recommendations. Please, be patient as this might take some time! :)")

        director = raw_input("The director: ")
        actor = raw_input("The actor: ")
        role = raw_input("The role of the actor: ")
        year = raw_input("The year: ")
        length = raw_input("The length of the movie: ")
        # length_l = raw_input("The largest length of the movie: ")
        # length_s = raw_input("The smallest length of the movie: ")
        genre = raw_input("The genre of the movie: ")
        if len(genre) != 0:
            genre_2 = raw_input("Another genre of the movie: ")
        review = raw_input("The lowest review score (1-10) of the movie you would want: ")
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
        

        #USED GENRE
        if(len(genre) != 0 and (not director) and (not actor) and (not role) and (not year) and (not length) and (not genre_2) and (not review) and (not production) and (not company)):
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

        #USED ACTOR
        if((not genre) and (not director) and len(actor) != 0 and (not role) and (not year) and (not length) and (not review) and (not production) and (not company)):
            l = ("\nTitle | Year | Actor | Actor Date of Birth:")
            sql = """SELECT m_title, m_year, a_name, a_dob
                    FROM actor, movies, appears
                    WHERE m_movieid = app_movieid
                    AND a_actorid = app_actorid
                    AND a_name LIKE ? """
            var = "%" + actor + "%"
            args = [var]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            if len(actor) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3])
                        print(l)

        #USED ACTOR AND GENRE
        if(len(genre) != 0 and (not director) and len(actor) != 0 and (not role) and (not year) and (not length) and (not genre_2) and (not review) and (not production) and (not company)):
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
        
        #USED GENRE AND YEAR
        if(len(genre) != 0 and (not director) and (not actor) and (not role) and len(year) != 0 and (not length) and (not review) and (not production) and (not company)):
            print("Enter 1 if you want to INCLUDE movies BEFORE " + year + " -or- Enter 2 if you want to INCLUDE movies AFTER " + year + " -or- Enter 0 for neither:") 
            year_2 = input()
            if year_2 == 0 and len(genre_2) == 0:
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND m_year = ?
                        ORDER BY g_genre;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 0 and len(genre_2) != 0:
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND m_year = ?
                        UNION 
                        SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND m_year = ?
                        ORDER BY g_genre;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year, genre_2, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 1 and len(genre_2) == 0:
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year < ? OR m_year = ?)
                        ORDER BY g_genre;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 1 and len(genre_2) != 0:
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year < ? OR m_year = ?)
                        UNION 
                        SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year < ? OR m_year = ?)
                        ORDER BY g_genre;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year, year, genre_2, year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 2 and len(genre_2) == 0:   
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year > ? OR m_year = ?)
                        ORDER BY g_genre;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 2 and len(genre_2) != 0:
                l = ("\nTitle | Year | Genre | Length:")
                sql = """SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year > ? OR m_year = ?)
                        UNION 
                        SELECT m_title, m_year, g_genre, m_length
                        FROM movies, genre
                        WHERE m_movieid = g_movieid
                            AND g_genre LIKE ?
                            AND (m_year > ? OR m_year = ?)
                        ORDER BY m_year;"""
                cur = _conn.cursor()
                cur.execute(sql, (genre, year, year, genre_2, year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)

        #USED DIRECTOR
        if((not genre) and len(director) != 0 and (not actor) and (not role) and (not year) and (not length) and (not review) and (not production) and (not company)):
            l = ("\nTitle | Year | Director:")
            sql = """SELECT m_title, m_year, d_name
                    FROM director, movies
                    WHERE d_name = m_director
                        AND d_name LIKE ?
                    GROUP BY m_title;"""
            var = "%" + director + "%"
            args = [var]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2])
                        print(l)

        #USED YEAR & year_2
        if((not genre) and (not director) and (not actor) and (not role) and len(year) != 0 and (not length) and (not review) and (not production) and (not company)):
            print("Enter 1 if you want to INCLUDE movies BEFORE " + year + " -or- Enter 2 if you want to INCLUDE movies AFTER " + year + " -or- Enter 0 for neither:") 
            year_2 = input()
            if year_2 == 0:
                l = ("\nTitle | Year | Actor | Director")
                sql = """SELECT distinct m_title, m_year, a_name, d_name
                        from director, movies, actor
                        where d_name = a_name
                            and m_director = d_name
                            and m_year = ?
                        GROUP BY a_name;"""
                cur = _conn.cursor()
                cur.execute(sql, (year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 1:
                l = ("\nTitle | Year | Actor | Director")
                sql = """SELECT distinct m_title, m_year, a_name, d_name
                        from director, movies, actor
                        where d_name = a_name
                            and m_director = d_name
                            and (m_year < ? OR m_year = ?)
                        GROUP BY a_name;"""
                cur = _conn.cursor()
                cur.execute(sql, (year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
            if year_2 == 2:
                l = ("\nTitle | Year | Actor | Director")
                sql = """SELECT distinct m_title, m_year, a_name, d_name
                        from director, movies, actor
                        where d_name = a_name
                            and m_director = d_name
                            and (m_year > ? OR m_year = ?)
                        GROUP BY a_name;"""
                cur = _conn.cursor()
                cur.execute(sql, (year, year,))
                rows = cur.fetchall()
                if len(rows) != 0:
                    print(l)
                    for row in rows:
                            l = (row[0], row[1], row[2], row[3])
                            print(l)
        #USED Review & Length & Year 
        if((not genre) and (not director) and (not actor) and (not role) and len(year) != 0 and len(length) != 0 and len(review) != 0 and (not production) and (not company)):
            l = ("\nTitle | Year | Length | Review IMDB | Review Rotten Tomato ")
            sql = """SELECT m_title, m_year, m_length, r_imdb, r_rottent
                    FROM movies, review
                    WHERE movies.m_movieid = review.r_movieid
                        AND review.r_imdb >= ?
                        AND r_rottent >= ?
                        AND m_length = ?
                        AND m_year = ?
                    ORDER BY m_year, r_imdb, m_length;"""
            cur = _conn.cursor()
            cur.execute(sql, (review, review, length, year,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3])
                        print(l)
        #USED REVIEW & YEAR
        if((not genre) and (not director) and (not actor) and (not role) and len(year) != 0 and (not length) and len(review) != 0 and (not production) and (not company)):
            l = ("\nTitle | Year | Length | Review IMDB | Review Rotten Tomato")
            sql = """SELECT m_title, m_year, m_length, r_imdb, r_rottent
                    FROM movies, review
                    WHERE movies.m_movieid = review.r_movieid
                        AND review.r_imdb >=  ?
                        AND r_rottent >= ?
                        AND m_year = ?
                    ORDER BY m_year, r_imdb, m_length;"""
            cur = _conn.cursor()
            cur.execute(sql, (review, review, year,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3])
                        print(l)
        #USED Review
        if((not genre) and (not director) and (not actor) and (not role) and (not year) and (not length) and len(review) != 0 and (not production) and (not company)):
            l = ("\nTitle | Year | Actor | Actor Role | Genre | Review IMDB | Review Rotten Tomato")
            sql = """SELECT m_title, m_year, a_name, app_role, g_genre, r_imdb, r_rottent
                    FROM movies, actor, appears, genre, review
                    WHERE m_movieid = app_movieid
                        AND movies.m_movieid = review.r_movieid
                        AND m_movieid = g_movieid
                        AND a_actorid = app_actorid
                        AND r_imdb >= ?
                        AND r_rottent >= ?
                    GROUP BY m_title, app_role
                    ORDER BY m_year DESC, r_rottent ASC, r_imdb ASC;"""
            cur = _conn.cursor()
            cur.execute(sql, (review, review,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                        print(l)
        #USED REVIEW & GENRE
        if(len(genre) != 0 and (not director) and (not actor) and (not role) and (not year) and (not length) and (not genre_2) and len(review) != 0 and (not production) and (not company)):
            l = ("\nTitle | Year | Genre | Review IMDB | Review Rotten Tomato")
            sql = """SELECT m_title, m_year, g_genre, r_imdb, r_rottent
                    from genre, movies, review
                        where r_movieid = m_movieid
                            and g_movieid = m_movieid
                            and r_imdb >= ?
                            and r_rottent >= ?
                            and g_genre = (select g_genre
                                            from genre
                                            where g_genre LIKE ?)
                    Order by m_title ASC;"""
            cur = _conn.cursor()
            cur.execute(sql, (review, review, genre,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4])
                        print(l)
        #USED COMPANY
        if((not genre) and (not director) and (not actor) and (not role) and (not year) and (not length) and (not review) and (not production) and len(company) != 0):
            l = ("\nTitle | Year | Actor | Actor Role | Movie Company")
            sql = """SELECT m_title, m_year, a_name, app_role, c_company
                    FROM actor, movies, company, appears
                    WHERE m_movieid = app_movieid	
                        AND a_actorid = app_actorid
                        AND m_company = c_company 
                        AND c_company IN (SELECT c_company
                                            FROM company
                                            WHERE c_company LIKE ? )
                    GROUP BY a_name
                    ORDER BY m_title ASC;"""
            var = "%" + company + "%"
            args = [var]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4])
                        print(l)
        
        #USED PRODUCTION                
        if((not genre) and (not director) and (not actor) and (not role) and (not year) and (not length) and (not review) and len(production) != 0 and (not company)):
            l = ("\nTitle | Year | Actor | Director | Movie Company")
            sql = """SELECT m_title, m_year, a_name, m_director, c_company
                    FROM company, movies, director, actor, appears, production
                    WHERE m_movieid = app_movieid	
                        AND a_actorid = app_actorid
                        AND m_company = c_company 
                        AND d_name = m_director
                        AND p_type = ? 
                        AND a_actorid = p_actorid
                        AND d_dirid = p_dirid
                    GROUP BY m_title, a_name;"""
            cur = _conn.cursor()
            cur.execute(sql, (production,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4])
                        print(l)
        #USED ROLE
        if((not genre )and (not director) and (not actor) and len(role) != 0 and (not year) and (not length) and (not review) and (not production) and (not company)):
            l = ("\nTitle | Year | Actor | Actor Role | Director | Movie Company")
            sql = """SELECT m_title, m_year, a_name, app_role, m_director, m_company, 
                    FROM appears, actor, movies
                    WHERE m_movieid = app_movieid	
                        AND a_actorid = app_actorid
                        AND app_role = ?;"""
            cur = _conn.cursor()
            cur.execute(sql, (role,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5])
                        print(l)
        # USED YEAR & DIRECTOR & ACTOR & ROLE & GENRE & REVIEW
        if(len(genre) != 0 and len(director) != 0 and len(actor) != 0 and len(role) != 0 and len(year) != 0 and (not length) and (not genre_2) and len(review) != 0 and (not production) and (not company)):
            l = ("\nTitle | Year | Actor | Actor Date of Birth | Actor Role | Director | Movie Company | Genre | Review IMDB | Review Rotten Toamtoes ")
            sql = """SELECT m_title, m_year, a_name, a_dob, app_role, d_name, c_company, g_genre, r_imdb, r_rottent
                    from actor, movies, appears, company, director, genre, review
                    where m_movieid = app_movieid
                        and app_actorid = a_actorid
                        and m_company = c_company
                        and m_director = d_name
                        and m_movieid = g_movieid
                        and m_movieid = r_movieid
                        and m_year = ?
                        and d_name = ?
                        and a_name = ?
                        and app_role = ?
                        and g_genre = ?
                        and r_imdb >= ?
                        and r_rottent >= ?
                    ORDER BY m_title, m_year, a_name, d_name;"""
            cur = _conn.cursor()
            cur.execute(sql, (year, director, actor, role, genre, review, review,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                        print(l)
        ##USED YEAR & DIRECTOR & ACTOR & ROLE & GENRE & REVIEW & LENGTH & PRODUCTION & COMPANY
        if len(year) != 0 and len(director) != 0 and len(actor) != 0 and len(role) != 0 and len(genre) != 0 and len(review) != 0 and len(length) != 0 and len(production) != 0 and len(company) != 0 and (not genre_2):
            l = ("\nTitle | Year | Movie Length | Actor | Actor Date of Birth | Actor Role | Director | Movie Company | Genre | Review IMDB | Review Rotten Toamtoes | Production")            
            sql = """SELECT m_title, m_year, m_length, a_name, a_dob, app_role, d_name, c_company, g_genre, r_imdb, r_rottent, p_type
                    from actor, movies, appears, company, director, genre, review
                    where m_movieid = app_movieid
                        and app_actorid = a_actorid
                        and m_company = c_company
                        and m_director = d_name
                        and m_movieid = g_movieid
                        and m_movieid = r_movieid
                        and p_dirid = d_dirid
                        and p_actorid = a_actorid
                        and m_year = ?
                        and d_name = ?
                        and a_name = ?
                        and app_role = ?
                        and g_genre = ?
                        and r_imdb >= ?
                        and r_rottent >= ?
                        and m_length = ?
                        and p_type = ?
                        and c_company = ?
                    ORDER BY m_title, m_year, a_name, d_name;"""
            cur = _conn.cursor()
            cur.execute(sql, (year, director, actor, role, genre, review, review, length, production, company,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                        print(l)
        # USED PRODUCTION AND DIRECTOR              ones that worked: 
        if((not genre) and len(director) != 0 and (not actor) and (not role) and (not year) and (not length) and (not review) and len(production) != 0 and (not company)):
            l = ("\nTtile | Year | Length | Director")
            sql = """select m_title, m_year, m_length, d_name
                    from movies, director, production
                    where d_name = p_dirname
                        and p_dirname = (select p_dirname
                                        from production
                                        where p_type LIKE ?
                                            and p_dirname LIKE ?)
                        and d_name = m_director;"""
            var = "%" + director + "%"
            args = [production, var]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3])
                        print(l)
        # USED PRODUCTION & ACTOR & DIRECTOR
        if((not genre) and len(director) != 0 and len(actor) != 0 and (not role) and (not year) and (not length) and (not review) and len(production) != 0 and (not company)):
            l = ("\n")
            ######### ^ come back to this line later
            sql = """select m_title, m_length, m_year, p_aname, p_dirname, p_type
                    from production, movies, actor, appears
                    where p_type LIKE ?
                        and p_aname LIKE ?
                        and p_dirname LIKE ?
                        and a_actorid = p_actorid
                        and a_actorid = app_actorid
                        and app_movieid = m_movieid
                    ORDER BY m_length ASC;"""
            var_1 = "%" + actor + "%"
            var_2 = "%" + director + "%"
            args = [production, var_1, var_2]
            cur = _conn.cursor()
            cur.execute(sql, args)
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5])
                        print(l)
        #Asks users if they w ant all info in Movie Night?
        print("\nWould you like to view all of the information in Movie Night? (Yes: Enter 1 -or- No: Enter 2)")
        answer = input()
        if answer == 1:
            sql = """SELECT m_title, m_year, a_name, app_role, a_dob, c_company, d_name, g_genre, r_imdb, r_rottent
                    from actor, movies, appears, company, director, genre, review
                    where m_movieid = app_movieid
                        and app_actorid = a_actorid
                        and m_company = c_company
                        and m_director = d_name
                        and m_movieid = g_movieid
                        and m_movieid = r_movieid
                    GROUP BY m_title;"""
            cur = _conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                        print(l)

        print("\nWould you like to search (Enter 1) -or- receive a recommendation again (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 4)?:")
        answer = input()
        if answer == 4:
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
####### INSERT FUNCTIONS ######################################################################################################################################
def insert_movies(_conn):
    try:
        t = raw_input("Enter the movie title:")
        id = raw_input("Enter the movie ID in this format -> tt# :")
        y = input("Enter the movie year:")
        l = input("Enter the movie length (in total minutes):")
        d = raw_input("Enter the movie director:")
        c = raw_input("Enter the movie company:")
        
        sql = """INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)"""
        cur = _conn.cursor()
        cur.execute(sql, (id, t, y, l, d, c,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def insert_actor(_conn):
    try:
        n = raw_input("Enter actor's first name and last name: ")
        id = raw_input("Enter the actor's ID in this format -> nm#########: ")
        dob = raw_input("Enter actor's date of birth in this format -> mm/dd/yyyy: ")
        
        sql = """INSERT INTO actor VALUES (?, ?, ?)"""
        cur = _conn.cursor()
        cur.execute(sql, (id, n, dob,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def insert_director(_conn):
    try:
        n = raw_input("Enter director's first name and last name: ")
        id = raw_input("Enter the director's ID in this format -> nm#########: ")

        sql = """INSERT INTO director VALUES (?, ?)"""
        cur = _conn.cursor()
        cur.execute(sql, (id, n,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def insert_genre(_conn):
    try:
        g = raw_input("Enter the movie's genre: ")
        id = raw_input("Enter the movie ID in this format -> tt# : ")

        sql = """INSERT INTO genre VALUES (?, ?)"""
        cur = _conn.cursor()
        cur.execute(sql, (id, g,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def insert_review(_conn):
    try:
        id = raw_input("Enter the movie ID in this format -> tt# : ")
        imdb = input("Enter the movie's IMDB review: ")
        rt = input("Enter the movie's IMDB review:")

        sql = """INSERT INTO review VALUES (?, ?, ?)"""
        cur = _conn.cursor()
        cur.execute(sql, (id, imdb, rt,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def insert_company(_conn):
    try:
        c = raw_input("Enter the company name: ")
        lo = raw_input("Enter the company's location in this format -> 2#### : ")

        sql = """INSERT INTO company VALUES (?, ?)"""
        cur = _conn.cursor()
        args = [c, lo]
        cur.execute(sql, args)
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
####### DELETE FUNCTIONS ######################################################################################################################################
def delete_movies(_conn):
    try:
        t = raw_input("Enter the movie title:")
        id = raw_input("Enter the movie ID in this format -> tt[integer value] :")
        y = input("Enter the movie year:")
        l = input("Enter the movie length (in total minutes):")
        d = raw_input("Enter the movie director:")
        c = raw_input("Enter the movie company:")
        
        sql = """DELETE FROM movies WHERE m_movieid = ?
                                        AND m_title = ?
                                        AND m_year = ?
                                        AND m_length = ?
                                        AND m_director = ?
                                        AND m_company = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id, t, y, l, d, c,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def delete_actor(_conn):
    try:
        n = raw_input("Enter actor's first name and last name: ")
        id = raw_input("Enter the actor's ID in this format -> nm[integer value]: ")
        dob = raw_input("Enter actor's date of birth: ")
        
        sql = """DELETE FROM actor WHERE a_actorid = ? AND a_name = ? AND a_dob = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id, n, dob,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def delete_director(_conn):
    try:
        n = raw_input("Enter director's first name and last name: ")
        id = raw_input("Enter the director's ID in this format -> nm#########: ")

        sql = """DELETE FROM director WHERE d_dirid = ? AND d_name = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id, n,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def delete_genre(_conn):
    try:
        g = raw_input("Enter the movie's genre: ")
        id = raw_input("Enter the movie ID in this format -> tt# : ")

        sql = """DELETE FROM genre WHERE g_movieid = ? AND g_genre = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id, g,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def delete_review(_conn):
    try:
        id = raw_input("Enter the movie ID in this format: ")
        imdb = input("Enter the movie's IMDB review: ")
        rt = input("Enter the movie's IMDB review:")

        sql = """DELETE FROM review WHERE r_movieid = ? AND r_imdb = ? AND r_rottent = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id, imdb, rt,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def delete_company(_conn):
    try:
        c = raw_input("Enter the company name: ")
        lo = raw_input("Enter the company's location: ")

        sql = """DELETE FROM company WHERE c_company = ? AND c_location = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (c, lo,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
####### UPDATE FUNCTIONS ######################################################################################################################################
def update_movies(_conn):
    try:
        print("What would you like to UPDATE? ")
        t = raw_input("Enter the movie title:")
        id = raw_input("Enter the movie ID in this format -> tt[integer value] :")
        y = input("Enter the movie year:")
        l = input("Enter the movie length (in total minutes):")
        d = raw_input("Enter the movie director:")
        c = raw_input("Enter the movie company:")
        print("What would you like to UPDATE the ABOVE information to?")
        t_1= raw_input("Enter the movie title:")
        id_1 = raw_input("Enter the movie ID in this format -> tt[integer value] :")
        y_1 = input("Enter the movie year:")
        l_1 = input("Enter the movie length (in total minutes):")
        d_1 = raw_input("Enter the movie director:")
        c_1 = raw_input("Enter the movie company:")

        sql = """UPDATE movies SET m_movieid = ?, m_title = ?, m_year = ?, m_length = ?, m_director = ?, m_company = ?
                                WHERE m_movieid = ? AND m_title = ? AND m_year = ? AND m_length = ? AND m_director = ? AND m_company = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id_1, t_1, y_1, l_1, d_1, c_1, id, t, y, l, d, c,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def update_actor(_conn):
    try:
        print("What would you like to UPDATE? ")
        n = raw_input("Enter actor's first name and last name: ")
        id = raw_input("Enter the actor's ID in this format -> nm[integer value]: ")
        dob = raw_input("Enter actor's date of birth: ")
        print("What would you like to UPDATE the ABOVE information to?")
        n_1 = raw_input("Enter actor's first name and last name: ")
        id_1 = raw_input("Enter the actor's ID in this format -> nm[integer value]: ")
        dob_1 = raw_input("Enter actor's date of birth: ")

        sql = """UPDATE actor SET a_actorid = ?, a_name = ?, a_dob = ? 
                                WHERE a_actorid = ? AND a_name = ? AND a_dob = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id_1, n_1, dob_1, id, n, dob,))
        _conn.commit()
        print("success")    
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def update_director(_conn):
    try:
        print("What would you like to UPDATE? ")
        n = raw_input("Enter director's first name and last name: ")
        id = raw_input("Enter the director's ID in this format -> nm#########: ")
        print("What would you like to UPDATE the ABOVE information to?")
        n_1 = raw_input("Enter director's first name and last name: ")
        id_1 = raw_input("Enter the director's ID in this format -> nm#########: ")

        sql = """UPDATE director SET d_dirid = ?, d_name = ? 
                                WHERE d_dirid = ? AND d_name = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id_1, n_1, id, n,))
        _conn.commit()
        print("success") 
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def update_genre(_conn):
    try:
        print("What would you like to UPDATE? ")
        g = raw_input("Enter the movie's genre: ")
        id = raw_input("Enter the movie ID in this format -> tt# : ")
        print("What would you like to UPDATE the ABOVE information to?")
        g_1 = raw_input("Enter the movie's genre: ")
        id_1 = raw_input("Enter the movie ID in this format -> tt# : ")

        sql = """UPDATE genre SET g_movieid = ?, g_genre = ? 
                                WHERE g_movieid = ? AND g_genre = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (id_1, g_1, id, g,))
        _conn.commit()
        print("success") 
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def update_review(_conn):
    try:
        print("What would you like to UPDATE? ")
        id = raw_input("Enter the movie ID in this format: ")
        imdb = input("Enter the movie's IMDB review: ")
        rt = input("Enter the movie's IMDB review:")
        print("What would you like to UPDATE the ABOVE information to?")
        id_1 = raw_input("Enter the movie ID in this format: ")
        imdb_1 = input("Enter the movie's IMDB review: ")
        rt_1 = input("Enter the movie's IMDB review:")

        sql = """UPDATE review SET r_movieid = ?, r_imdb = ?, r_rottent = ?
                                WHERE r_movieid = ? AND r_imdb = ? AND r_rottent = ? ;"""
        cur = _conn.cursor()
        cur.execute(sql, (id_1, imdb_1, rt_1, id, imdb, rt,))
        _conn.commit()
        print("success")
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
def update_company(_conn):
    try:
        print("What would you like to UPDATE? ")
        c = raw_input("Enter the company name: ")
        lo = raw_input("Enter the company's location: ")
        print("What would you like to UPDATE the ABOVE information to?")
        c_1 = raw_input("Enter the company name: ")
        lo_1 = raw_input("Enter the company's location: ")
        
        sql = """UPDATE company SET c_company = ?, c_location = ?
                                    WHERE c_company = ? AND c_location = ?;"""
        cur = _conn.cursor()
        cur.execute(sql, (c_1, lo_1, c, lo,))
        _conn.commit()
        print("success")
    except Error as e:        
        _conn.rollback()        
        print(e)    
        print("++++++++++++++++++++++++++++++++++")
####### MODIFY FUNCTION ######################################################################################################################################
def modify(_conn):
    try:
        # print("IN modify function")
        print("Thank you for modifying the Movie Night so it is an up-to-date catalog! :)")
        print("Would you like to INSERT data (Enter 1) -or DELETE data (Enter 2) -or- UPDATE data (Enter 3)?:")
        ans = input()
        if ans == 1: #INSERT
            print("What information do you want to INSERT?" + "\n" + "1. Movie" + "\n" + "2. Actor" + "\n" + "3. Director" + "\n" + "4. Genre" + "\n" + "5. Review" + "\n" + "6. Company")
            insert = input()
            if insert == 1: #MOVIES
                insert_movies(_conn)
            if insert == 2: #ACTOR
                insert_actor(_conn)
            if insert == 3: #DIRECTOR
                insert_director(_conn)
            if insert == 4: # GENRE
                insert_genre(_conn)
            if insert == 5: # REVIEW
                insert_review(_conn)
            if insert == 6: # COMPANY
                insert_company(_conn)
        if ans == 2: #DELETE
            print("What information do you want to DELETE?" + "\n" + "1. Movie" + "\n" + "2. Actor" + "\n" + "3. Director" + "\n" + "4. Genre" + "\n" + "5. Review" + "\n" + "6. Company")
            delete = input()
            if delete == 1: #MOVIES
                delete_movies(_conn)
            if delete == 2: #ACTOR
                delete_actor(_conn)
            if delete == 3: #DIRECTOR
                delete_director(_conn)
            if delete == 4: # GENRE
                delete_genre(_conn)
            if delete == 5: # REVIEW
                delete_review(_conn)
            if delete == 6: # COMPANY
                delete_company(_conn)
        if ans == 3: #UPDATE
            print("What information do you want to UPDATE?" + "\n" + "1. Movie" + "\n" + "2. Actor" + "\n" + "3. Director" + "\n" + "4. Genre" + "\n" + "5. Review" + "\n" + "6. Company")
            update = input()
            if update == 1: #MOVIES
                update_movies(_conn)
            if update == 2: #ACTOR
                update_actor(_conn)
            if update == 3: #DIRECTOR
                update_director(_conn)
            if update == 4: # GENRE
                update_genre(_conn)
            if update == 5: # REVIEW
                update_review(_conn)
            if update == 6: # COMPANY
                update_company(_conn)

        print("Would you like to search (Enter 1) -or- receive a recommendation again (Enter 2) -or- modify the movie system's information (Enter 3) -or- leave Movie Night (Enter 4)?:")
        answer = input()
        if answer == 4:
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