import mysql.connector
import datetime
import random

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
        if(len(names) == 0):
            return False
        return names[0][0] + " " + names[0][1]

    def find_patient_email(self, patient_NHS_number):
        self.mycursor.execute("SELECT Email FROM Patients WHERE PatientNHSNumber = %d;" %(patient_NHS_number,))
        email = self.mycursor.fetchall()
        if(len(email) == 0):
            return false
        return email[0][0]

    def add_new_prescription(self, patient_NHS_number, prescription_information):
        try:
            if(prescription_information.RepeatPrescription == 'Y' or prescription_information.RepeatPrescription == 'y'):
                self.mycursor.execute("INSERT INTO Prescriptions VALUES (NULL, %d, '%s', '%s', '%s', '%s', '%s', b'1', NULL);" %(patient_NHS_number, prescription_information.MedicineName, prescription_information.Dose, int(prescription_information.TimesPerDay), prescription_information.StartDate, int(prescription_information.Duration),))
            else:
                self.mycursor.execute("INSERT INTO Prescriptions VALUES (NULL, %d, '%s', '%s', '%s', '%s', '%s', b'0', NULL);" %(patient_NHS_number, prescription_information.MedicineName, prescription_information.Dose, int(prescription_information.TimesPerDay), prescription_information.StartDate, int(prescription_information.Duration),))
            self.mydb.commit()
        except Exception as e:
            print("Couldn't add prescription to database")
            raise

    def add_new_prescription_string(self, patient_NHS_number, prescription_information):
        try:
            self.mycursor.execute("INSERT INTO Prescriptions VALUES (NULL, %d, '%s', '%s', '%s', '%s', '%s', b'1', NULL);" %(patient_NHS_number, prescription_information, "125 mg", random.randint(3,5), datetime.datetime.now().isoformat(), random.randint(1,10),))
            self.mydb.commit()
        except Exception as e:
            print("Couldn't add prescription to database")
            raise


    def find_medicine_info(self, patient_NHS_number):
        self.mycursor.execute("SELECT Medicines.MedicineName, Medicines.Stock, RowNumber, ColumnNumber FROM Medicines RIGHT JOIN Prescriptions ON Medicines.MedicineName = Prescriptions.MedicineName WHERE Prescriptions.PatientNHSNumber = %d AND (Prescriptions.CollectionDate IS NULL OR (Prescriptions.RepeatPrescription = b'1' AND CURDATE() > DATE_ADD(Prescriptions.CollectionDate, INTERVAL (Prescriptions.Duration-1) DAY)));" %(patient_NHS_number,))
        result = self.mycursor.fetchall()
        if(len(result) > 0):
            return result[0]
        return False

    def update_collected_medicine(self, medicine_name, patient_NHS_number):
        Date = datetime.datetime.now().isoformat()
        self.mycursor.execute("UPDATE Prescriptions SET CollectionDate = '%s' WHERE MedicineName = '%s' and PatientNHSNumber = %d;" %(Date, medicine_name, patient_NHS_number,))

    def add_patient_to_database(self, patient_details):
        if(patient_details["Discount"] == 'Y' or patient_details["Discount"] == 'y'):
            self.mycursor.execute("INSERT INTO Patients VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', b'1');" %(patient_details["NHSNumber"], patient_details["DoctorID"], patient_details["FirstName"], patient_details["Surname"], patient_details["DoB"], patient_details["Email"], patient_details["Address"],))
        else:
            self.mycursor.execute("INSERT INTO Patients VALUES (%d, %d, '%s', '%s', '%s', '%s', '%s', b'0');" %(patient_details["NHSNumber"], patient_details["DoctorID"], patient_details["FirstName"], patient_details["Surname"], patient_details["DoB"], patient_details["Email"], patient_details["Address"],))
        self.mydb.commit()

    def find_used_NHS_numbers(self):
        self.mycursor.execute("SELECT PatientNHSNumber FROM Patients;")
        return self.mycursor.fetchall() #Convert to list

    def check_doctor_email(self, email):
        self.mycursor.execute("SELECT COUNT(Email) FROM Doctors WHERE Email = '%s';" %(email,))
        if(self.mycursor.fetchall()[0] > 0):
            return True
        return False

    def check_medicine_in_stock(self, medicine_name):
        self.mycursor.execute("SELECT Stock from Medicines WHERE MedicineName = '%s';" %(medicine_name,))
        if(self.mycursor.fetchall()[0] > 0):
            return True
        return False

    def update_medicine_collection(self, data):
        self.mycursor.execute("UPDATE Prescriptions SET CollectionDate = CURDATE() WHERE MedicineName = '%s' AND PatientNHSNumber = %d;" %(data.MedicineName, int(data.NHSNumber), ))
        self.mycursor.execute("UPDATE Medicines SET Stock = Stock - 1 WHERE MedicineName = '%s' AND Stock > 0;" %(data.MedicineName, ))
        self.mydb.commit()
