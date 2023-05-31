import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                hashedPassword TEXT NOT NULL)''')
        self.conn.commit()


    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None


def insert_user(username, hashed_password):
    # Create an instance of the Database class
    db = Database('database.db')

    try:
        # Connect to the database
        db.connect()

        # Insert data into the users table
        db.cursor.execute('''INSERT INTO users (username, hashedPassword)
                            VALUES (?, ?)''', (username, hashed_password))

        # Commit the changes
        db.conn.commit()

        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the connection
        db.close()

