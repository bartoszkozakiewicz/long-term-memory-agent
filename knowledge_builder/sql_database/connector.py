import mysql.connector
import os
import load_dotenv

load_dotenv.load_dotenv()

class Connector:
    def __init__(self):
        self.password=  os.environ.get("SQL_PASS")
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=self.password,
            database="PeopleDB"
            )

    def __enter__(self):
        return self.db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.db.commit()
        self.db.close()
        # self.db.cursor().close()

        if exc_type == Exception:
            raise Exception("Exception occured: ", exc_val)