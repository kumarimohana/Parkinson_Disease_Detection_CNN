import mysql.connector

# Function to create users table
def create_users_table():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            database='parkinson',
            user='root',
            password='system',
            auth_plugin='mysql_native_password',
            connect_timeout=30  # Increase connection timeout
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                date DATE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print("Error creating users table:", e)

# Call the function to create the users table
create_users_table()
import mysql.connector

def create_healthform_table():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            database='parkinson',
            user='root',
            password='system',
            auth_plugin='mysql_native_password',
            connect_timeout=30  # Increase connection timeout
        )
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS healthform (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                phonenumber VARCHAR(15) NOT NULL,
                bloodPressure VARCHAR(20) NOT NULL,
                bloodSugar VARCHAR(20) NOT NULL,
                healthHistory TEXT NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print("Error creating healthform table:", e)

# Call the function to create the healthform table
create_healthform_table()

