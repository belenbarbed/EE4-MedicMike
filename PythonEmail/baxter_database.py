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
        self.mycursor = self.mydb.cursor()

    def get_number_waiting_packages(self, email_address):
        self.mycursor.execute("SELECT COUNT(*) FROM packages INNER JOIN users ON packages.CollegeID = users.CollegeID WHERE packages.CollectionDate IS NULL AND users.Email = '%s';" % (email_address,))
        return self.mycursor.fetchall()[0][0]

    def add_arrived_package(self, CIDNumber, Address):
        self.mycursor.execute("SELECT ParcelLocation FROM packages WHERE CollectionDate IS NULL;")
        used_slots = self.mycursor.fetchall()
        used_slots = [i[0] for i in used_slots]
        for x in range(1, NumberSlots + 1):
            if x not in used_slots:
                Time = datetime.datetime.now()
                ArrivalDate = Time.strftime("%Y-%m-%d")
                ArrivalTime = Time.strftime("%H:%M:%S")
                self.mycursor.execute("INSERT INTO packages VALUES (NULL, %d,'%s',%d,'%s','%s', b'0', NULL, NULL);" % (CIDNumber, Address, x, ArrivalDate, ArrivalTime,))
                self.mydb.commit()
                return x

    def find_package_slot(self, CIDNumber):
        print CIDNumber
        self.mycursor.execute("SELECT ParcelLocation from packages WHERE CollegeID = %d AND CollectionDate IS NULL;" % (CIDNumber,)) # TODO: What if no package is found
        return self.mycursor.fetchall()[0][0]

    def update_collected_package(self, CIDNumber, PackageSlot):
        Time = datetime.datetime.now()
        CollectionDate = Time.strftime("%Y-%m-%d")
        CollectionTime = Time.strftime("%H:%M:%S")
        self.mycursor.execute("UPDATE packages SET CollectionDate = '%s', CollectionTime = '%s' WHERE CollegeID = %d AND ParcelLocation = %d;" %(CollectionDate, CollectionTime, CIDNumber, PackageSlot,))

    def update_notification_state(self, CIDNumber, PackageSlot, Notified):
        self.mycursor.execute("UPDATE packages SET Notified = b'%s' WHERE CollegeID = %d AND ParcelLocation = %d AND CollectionDate IS NOT NULL;" %(Notified, CIDNumber, PackageSlot,))

    def find_person_name(self, CIDNumber = 0, email = " "):
        self.mycursor.execute("SELECT FirstName, Surname FROM users WHERE CollegeID = %d OR Email = '%s';" %(CIDNumber, email,))
        names = self.mycursor.fetchall()
        return names[0][0] + " " + names[0][1]

    def find_person_email(self, CIDNumber):
        self.mycursor.execute("SELECT Email FROM users WHERE CollegeID = %d;" %(CIDNumber,))
        return self.mycursor.fetchall()[0][0]
