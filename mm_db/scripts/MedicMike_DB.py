#!/usr/bin/env python
import rospy, thread, time, random
import email_handler, database_handler
from mm_db.msg import DB_output
from mm_db.msg import FR_message
from mm_db.msg import OCR_message
from mm_db.msg import Prescription_message
from mm_db.msg import Collect_message

class MedicMikeDB:
    def __init__(self):
        self.mike_db = database_handler.BaxterSqlDatabase('localhost', 'root', 'root','Baxter')
        self.mike_email = email_handler.EmailHandler()
        rospy.init_node('Database', anonymous=True)
        rospy.Subscriber("FR_DB_Channel", FR_message, self.__FRcallback)
        rospy.Subscriber("OCR_DB_Channel", OCR_message, self.__OCRcallback)
        rospy.Subscriber("Collected_Channel", Collect_message, self.__Collectcallback)
        self.pub = rospy.Publisher("DB_Move_Channel", DB_output, queue_size=10)

    def alert_listener(self):
        rospy.spin()

    def __FRcallback(self, data):
        patient_NHS_number = data.NHSNumber
        if(patient_NHS_number != 0):
            self.__find_and_publish_medicine_info(patient_NHS_number)

    def __OCRcallback(self, data):
        try:
            patient_record = self.__create_patient_record(data)
            #prescription = data.Prescription_Info              - CHANGING MESSAGE FORMAT
            NHSNumber = self.__add_new_patient_to_database(patient_record)
            #self.mike_db.add_new_prescription(NHSNumber, prescription)
            self.mike_db.add_new_prescription_string(NHSNumber, data.Prescription_Info)
            self.__find_and_publish_medicine_info(NHSNumber)
        except Exception as e:
            print(e)
            print("Couldn't add patient information.")


    def __Collectcallback(self, data):
        print("Updating")
        self.mike_db.update_medicine_collection(data)
        print("Updated")

    def __find_and_publish_medicine_info(self, patient_NHS_number):
        medicine_info = self.__retrieve_medicine_from_database(patient_NHS_number)
        patient_name = self.mike_db.find_patient_name(patient_NHS_number)
        self.__publish_medicine_info(medicine_info, patient_name, patient_NHS_number)

    def __add_new_patient_to_database(self, patient_record):
        if(patient_record["NHSNumber"] == 0):
            NHSNumber = self.__generate_NHS_number()
            patient_record["NHSNumber"] = NHSNumber
        else:
            NHSNumber = patient_record["NHSNumber"]
        if(self.mike_db.find_patient_name(NHSNumber) == False):
            self.mike_db.add_patient_to_database(patient_record)
        return NHSNumber

    # In a real implementation this number would be looked up. As we don't have access to the NHS
    # database (and because NHS numbers are a bit personal) we'll randomly generate it
    def __generate_NHS_number(self):
        used_numbers = self.mike_db.find_used_NHS_numbers();
        number = random.randint(1, 1000000000)
        while(number in used_numbers):
            number = random.randint(1, 1000000000)
        return number

    def __create_patient_record(self, data):
        patient_record = {}
        try:
            patient_record["NHSNumber"] = int(data.NHSNumber)
            try:
                if(data.DoctorID != ""):
                    patient_record["DoctorID"] = int(data.DoctorID)
                else:
                    patient_record["DoctorID"] = 1
                    
                if(data.FirstName != ""):
                    patient_record["FirstName"] = data.FirstName
                else:
                    patient_record["FirstName"] = "Joe"

                if(data.Surname):
                    patient_record["Surname"] = data.Surname
                else:
                    patient_record["Surname"] = "Bloggs"

                if(data.DoB != ""):
                    patient_record["DoB"] = data.DoB
                else:
                    patient_record["DoB"] = "1992-10-7"

                if(data.Email != ""):
                    patient_record["Email"] = data.Email
                else:
                    patient_record["Email"] = "owen.harcombe@gmail.com"

                if(data.Address != ""):
                    patient_record["Address"] = data.Address
                else:
                    patient_record["Address"] = "EEE Building, Kensington, London, SW7 2BS"

                if(data.Discount != ""):
                    patient_record["Discount"] = data.Discount
                else:
                    patient_record["Discount"] = 'N'

                return patient_record
            except Exception as e:
                print("Error converting Doctor ID to an Int!")
                raise
        except Exception as e:
            print("Error converting NHSNumber to an Int!")
            raise

    def __create_prescription(self, data):
        prescription = Prescription_message()
        prescription.MedicineName = data[1][1]
        prescription.Dose = data[1][2]
        prescription.TimesPerDay = int(data[1][3])
        prescription.StartDate = data[1][4]
        prescription.Duration = int(data[1][5])
        prescription.RepeatPrescription = data[1][6]
        return prescription

    def __retrieve_medicine_from_database(self, patient_NHS_number):
        medicine_info = self.mike_db.find_medicine_info(patient_NHS_number)
        return medicine_info

    def __publish_medicine_info(self, medicine_info, patient_name, patient_NHS_number):
        msg = DB_output()
        msg.NHSNumber = patient_NHS_number
        msg.PatientName = patient_name
        if(medicine_info == False):
            msg.MedicineName = "N/A"
            msg.Row = 0
            msg.Column = 0
        elif(medicine_info[1] == 0):
            msg.MedicineName = "Out Of Stock"
            msg.Row = 0
            msg.Column = 0
        else:
            msg.MedicineName = medicine_info[0]
            msg.Row = medicine_info[2]
            msg.Column = medicine_info[3]
        rospy.loginfo(msg)
        self.pub.publish(msg)

    def email_listener(self):
        while(True):
            mail_requests = self.mike_email.check_for_new_mail()
            for email in mail_requests: # Iterate through all emails and add new prescriptions to database
                if(self.mike_db.check_doctor_email(email[0])):
                    self.mike_db.add_new_prescription(int(email[1][0]), self.__create_prescription(email))
                    if(self.mike_db.check_medicine_in_stock(email[1][1])):
                        PatientNHSNumber = int(email[1][0])
                        self.mike_email.send_email(self.mike_db.find_patient_name(PatientNHSNumber), self.mike_db.find_patient_email(PatientNHSNumber))
            time.sleep(60)      # Wait 1 minute before trying again

# Create instance and run email and alert in seperate threads
medic_mike_db = MedicMikeDB()
thread.start_new_thread(medic_mike_db.email_listener())
thread.start_new_thread(medic_mike_db.alert_listener())
