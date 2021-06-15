import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "pass",
                           db = "seleksiirk5")
    c = conn.cursor()

    return c, conn

def insertRecord(name, startTime, route, deliveryDuration, finishTime, cost):
    c, conn = connection()
    sql = f"INSERT INTO deliveries ({name}, {startTime}, {route}, {deliveryDuration}, {finishTime}, {cost})"

    c.execute(sql)
    conn.commit()

def searchRecord(name, deliveryDate):
    c, conn = connection()

    if name == '':
        #CAPEEE