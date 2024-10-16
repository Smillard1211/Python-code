import pymysql as h
import pymysql.cursors

"""
basics for this program
- used as an import for other files
- 'conn' is the connection used from pymysql

example conn
-------------------------------------------------
conn = h.connect(
    host = hostName,
    user = userName,
    password = password,
    db = database,
    charset = 'utf8mb4',

host = host name of the database
user = user for the database
password = the password for the database
db = database name
- each of these are counted as a string in python, so they should be declared as such
--------------------------------------------------
more clearer definition in the pymysql documentation online
"""



#update current values 
# set = value to be changed
# ID = distinct value to be found
# IDName = name of the ID to be found(AKA the column)
def update(conn, set, table, ID, IDName):
    try:
        with conn.cursor() as cursor:
            query = f"update {table} set {set} where {IDName} = {ID}"
            cursor.execute(query)
            conn.commit()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")    
    finally:
        conn.close()

#gets the values from the database into a entry list
def get(conn, table):
    ret = []
    try:
        with conn.cursor() as cursor:
           cursor.execute(f"select * from {table}")
           ret = cursor.fetchall()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")    
    finally:
        conn.close()
    return ret

#be able to insert one type of row into a database
def insertRow(conn, table, header, values):
    try:
        with conn.cursor() as cursor:
           query = insertQuery(table, header)
           
           conn.ping(reconnect=True)
           cursor.execute(query, values)
           conn.commit()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")    
    finally:
        conn.close()
        
#***be very carful with this function***
#takes a table column and delete to be used in a query to delete that row
#deletes all rows that contain the 'delete' value in the column given
def deleteRow(conn, table, column, delete):
    try: 
        with conn.cursor() as cursor:
            query = f"delete from {table} where {column} = {delete};"
            cursor.execute(query)
            conn.commit()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        conn.close()


#makes the query for the insert function
def insertQuery(table, header):
    sql = f"insert into {table}("
    temp = 0
    for i in range(0, len(header)):
        temp += 1
        sql += f"{header[i]}"
        if temp < len(header):
            sql += ", "

    sql += ") values ("
    temp = 0
    for i in range(0, len(header)):
        temp += 1
        sql += "%s"
        if temp < len(header):
            sql += ", "
    sql += ")"
    return sql

#prints the entry from query result using the result and a specific value
def printEntry(list, value):
    for entry in list:
        print(f"{value}: {entry[value]}")



