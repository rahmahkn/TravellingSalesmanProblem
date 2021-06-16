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
    sql = f"INSERT INTO deliveries VALUES ('{name}', '{startTime}', '{route}', {deliveryDuration}, '{finishTime}', {cost})"

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

    print(result[0])
    print(result[1])

# Driver
# insertRecord('Syifa','2021-06-16 12:05:12','Rdalf->bkfa',43.3,'2021-06-17 10:40:12',565.1)
searchRecord('','2021-06-16')