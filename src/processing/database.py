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
    sql = f'''INSERT INTO deliveries
            (name, startTime, route, deliveryDuration, finishTime, cost)
            VALUES ('{name}', '{startTime}', '{route}', {deliveryDuration}, '{finishTime}', {cost})'''

    c.execute(sql)
    conn.commit()

def searchRecord(courierName, date):
    c, conn = connection()

    if courierName == '':
        sql = f"SELECT * FROM deliveries WHERE DATE(startTime) = '{date}'"
    else:
        if date == '':
            sql = f"SELECT * FROM deliveries WHERE name = '{courierName}'"
        else:
            sql = f"SELECT * FROM deliveries WHERE DATE(startTime) = '{date}' and name = '{courierName}'"

    c.execute(sql)
    result = list(c.fetchall())
    
    for i in range (len(result)):
        result[i] = list(result[i])
        result[i][3] = result[i][3].replace('->', '→')

    return result