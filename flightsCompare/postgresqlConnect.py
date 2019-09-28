import psycopg2
from datetime import datetime


# connect to db
def connectdb():
    con = psycopg2.connect(
        host = "localhost",
        port = "32778",
        database = "postgres",
        user = "postgres",
        password = "postgres",
    )

    return con

def querydb(table):
    # connect to db
    con = connectdb()

    # cursor
    cur = con.cursor()

    # execute query
    # city, price 
    cur.execute("SELECT id, date, city, price FROM {}".format(table))

    rows = cur.fetchall()

    for x in rows:
        # print(f"city {x[0]} price {x[1]}")
        print("id {} date {} city {} price {}".format(x[0], x[1], x[2],x [3]))

    # close cursor
    cur.close()

    # close connection
    con.close()

 
# original working version
# def updatedb(date, city, price):
#     # connect to db
#     con = connectdb()
#     cur = con.cursor()
#     cur.execute("INSERT INTO flights (date, city, price) VALUES (%s, %s, %s)", (date, city, price))

#     con.commit()

#     # close connection
#     con.close()

def updatedb(Results):
    # connect to db
    con = connectdb()
    cur = con.cursor()
    for result in Results:
        cur.execute("INSERT INTO flights (date, city, price) VALUES (%s, %s, %s)", (result['date'], result['city'], result['price']))

    con.commit()

    # close connection
    con.close()

def createtable(tablename):
    con = connectdb()
    cur = con.cursor()
    cur.execute("CREATE TABLE {} (id SERIAL UNIQUE PRIMARY KEY NOT NULL, date CHAR(10), city CHAR(12), price CHAR(7))".format(tablename))
    con.commit()
    con.close()

def droptable(tablename):
    con = connectdb()
    cur = con.cursor()
    cur.execute("DROP TABLE {}".format(tablename))
    con.commit()
    con.close()

# untested, to show db connections
def connections(db):
    con = connectdb()
    cur = con.cursor()
    cur.execute("SELECT * FROM pg_stat_activity WHERE datname = '{}'".format(db))

if __name__ == "__main__":
    table = "flights"
    createtable(table)
    # updatedb(datetime.now().date(), "Paris", 32.00)
    # querydb(table)
    # droptable(table)
