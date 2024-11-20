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

curr = conn.cursor()

