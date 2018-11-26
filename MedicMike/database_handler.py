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

    def find_patient_name(self, patient_NHS_number):
        self.mycursor.execute("SELECT FirstName, Surname FROM Patients WHERE PatientNHSNumber = %d;" %(patient_NHS_number,))
        names = self.mycursor.fetchall()
        return names[0][0] + " " + names[0][1]

    def add_new_prescription(self, prescription_information):
        repeat = "b'0'"
        if(prescription_information[7] == "Y"):
            repeat = "b'1'"
        self.mycursor.execute("INSERT INTO Prescriptions VALUES (NULL, %d, '%s', '%s', %d, '%s', %d, '%s');" %(prescription_information[1], prescription_information[2], prescription_information[3], prescription_information[4], prescription_information[5], prescription_information[6], repeat, ))
        self.mydb.commit()

    def find_medicine_info(self, patient_NHS_number):
        self.mycursor.execute("SELECT Medicines.MedicineName, RowNumber, ColumnNumber FROM Medicines RIGHT JOIN Prescriptions ON Medicines.MedicineName = Prescriptions.MedicineName WHERE Prescriptions.PatientNHSNumber = %d AND (Prescriptions.CollectionDate IS NOT NULL OR (Prescriptions.RepeatPrescription = b'1' AND CURDATE() > DATE_ADD(Prescriptions.CollectionDate, INTERVAL (Prescriptions.Duration-1) DAY)));" %(patient_NHS_number,))
        if(len(self.mycursor.fetchall()) > 0):
            print self.mycursor.fetchall()[0]
            return self.mycursor.fetchall()[0]
        return False

    def update_collected_medicine(self, medicine_name, patient_NHS_number):
        Time = datetime.datetime.now()
        self.mycursor.execute("UPDATE Prescriptions SET CollectionDate = '%s' WHERE MedicineName = '%s' and PatientNHSNumber = %d;" %(Time, medicine_name, patient_NHS_number,))

    def add_patient_to_database(self, patient_details):
        self.mycursor.execute("INSERT INTO Patients VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', '%s');" %(patient_details["NHSNumber"], patient_details["DoctorID"], patient_details["FirstName"], patient_details["Surname"], patient_details["DoB"], patient_details["Email"], patient_details["Address"], patient_details["Discount"], ))
        self.mydb.commit()

    def find_used_NHS_numbers(self):
        self.mycursor.execute("SELECT PatientNHSNumber FROM Patients;")
        return self.mycursor.fetchall() #Convert to list
