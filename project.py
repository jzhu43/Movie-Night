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
        
        #USED GENRE AND YEAR
        if len(genre) != 0 and len(year) != 0:
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
        if len(year) != 0:
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
        if len(review) != 0 and len(length) != 0 and len(year) != 0:
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
        if len(review) != 0 and len(year) != 0:
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
        if len(review) != 0:
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
        if len(review) != 0 and len(genre) != 0:
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
        if len(company) != 0:
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
        if len(production) != 0:
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
        if len(role) != 0:
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
        if len(year) != 0 and len(director) != 0 and len(actor) != 0 and len(role) != 0 and len(genre) != 0 and len(review) != 0:
            sql = """SELECT m_title, m_year, a_name, app_role, a_dob, c_company, d_name, g_genre, r_imdb, r_rottent
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
                        and review = ?
                    ORDER BY m_title, m_year, a_name, d_name;"""
            cur = _conn.cursor()
            cur.execute(sql, (year, director, actor, role, genre, review,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                        print(l)
        # USED PRODUCTION AND DIRECTOR
        if len(production) != 0 and len(director) != 0:
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
        if len(production) != 0 and len(actor) != 0 and len(director) != 0:
            l = ("\n")
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
        #
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
            cur.execute(sql, (role,))
            rows = cur.fetchall()
            if len(rows) != 0:
                print(l)
                for row in rows:
                        l = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
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