import mysql.connector

class BaxterSqlDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            database = self.database_name
        )
        self.mydbcursor = self.mydb.cursor()

    def get_number_waiting_packages(self, email_address):
        self.mydbcursor.execute("SELECT COUNT(*) FROM packages INNER JOIN users ON packages.CollegeID = users.CollegeID WHERE packages.CollectionDate IS NULL AND users.Email = '%s';" % (email_address,))
        return mycursor.fetchall()
