from dbcm import DBCM

class DBOperations():     
    """
    The DBOPerations class represents the database functions of the program.
    """
    def __init__(self, db_name):
        self.db_name = db_name
    
    def initialize_db(self):
        """
        The initialize_db class represents the class that makes the database and tables.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS WeatherData
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                                    date TEXT UNIQUE NOT NULL, 
                                    location TEXT NOT NULL, 
                                    min_REAL NOT NULL, 
                                    avg_temp temp REAL NOT NULL, 
                                    max_temp REAL NOT NULL);"""
                                )

    def fetch_data(self):
        """
        The fetch_data method returns all the rows in the WeatherData table.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("SELECT date, avg_temp from WeatherData")
            return cursor.fetchall()

    def save_data(self, data):
        """
        The save_data method saves and inserts data into the WeatherData table.
        """
        with DBCM(self.db_name) as cursor:
            for k, value in data.items():
                values = (k, 'Winnipeg, MB',  value['Max'], value['Min'], value['Mean'])
                cursor.execute("""
                                INSERT OR IGNORE INTO WeatherData (date, location, min_temp, max_temp, avg_temp)
                                VALUES (?, ?, ?, ?, ?)
                               """, values)

    def purge_data(self):
        """
        The purge_data method deletes data from WeatherData table.
        """
        with DBCM(self.db_name) as cursor:
            cursor.execute("DELETE FROM WeatherData")
