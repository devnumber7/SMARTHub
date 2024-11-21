#module imports from mariadb connector
import mariadb
import sys

#connect to mariadb
try:
    conn = mariadb.connect(
        user="test",
        password="SMART",
        host="localhost",
        port=3306,
        database="SMART"
    )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

print("Connection to MariaDB Platform successful!")

cur = conn.cursor()

query = "SELECT * FROM test"

device_list =[]

try :
    cur.execute(query)

    for (row) in cur:
        device_list.append([row[0], row[1]])


    print("Devices Array:")
    for device in device_list:
        print(device)

except mariadb.Error as e:
    print(f"Error: {e}")









