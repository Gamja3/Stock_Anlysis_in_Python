import pymysql

connection = pymysql.connect(host='localhost', port=3307, db='INVESTAR',
                             user='root', password='1234', autocommit=True)

cursor = connection.cursor()
cursor.execute("select VERSION();")
result = cursor.fetchone()

print("MariaDB version : {}".format(result))

connection.close()