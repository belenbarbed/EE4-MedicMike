import mysql.connector
import datetime

NumberSlots = 10

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
        return self.mycursor.fetchall()

    def add_arrived_package(self, CIDNumber, Address):
        self.mydbcursor.execute("SELECT ParcelLocation FROM packages WHERE CollectionDate IS NULL;")
        used_slots = self.mycursor.fetchall()
        for x in range(1, NumberSlots + 1):
            if x not in used_slots:
                Time = datetime.datetime.now()
                ArrivalDate = Time.strftime("%Y-%m-%d")
                ArrivalTime = Time.strftime("%H:%M:%S")
                self.mydbcursor.execute("INSERT INTO packages (CollegeID, Address, ParcelLocation, ArrivalDate, ArrivalTime) VALUES (%d,%s,%d,'%s','%s');" % (CIDNumber, Address, x, ArrivalDate, ArrivalTime,))
                return x

    def find_package_slot(self, CIDNumber):
        self.mydbcursor.execute("SELECT ParcelLocation from packages WHERE CollegeID = %d AND CollectionDate IS NOT NULL;" %(CIDNumber,))
        return self.mycursor.fetchall()

    def update_collected_package(self, CIDNumber, PackageSlot):
        Time = datetime.datetime.now()
        CollectionDate = Time.strftime("%Y-%m-%d")
        CollectionTime = Time.strftime("%H:%M:%S")
        self.mydbcursor.execute("UPDATE packages SET CollectionDate = '%s', CollectionTime = '%s' WHERE CollegeID = &d AND ParcelLocation = %d;" %(CollectionDate, CollectionTime, CIDNumber, PackageSlot,))
