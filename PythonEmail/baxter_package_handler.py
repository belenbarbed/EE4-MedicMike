#!/usr/bin/env python
import rospy, thread
import baxter_database, baxter_email_handler
from post_bot_pat.msg import PackageInfoIn
from post_bot_pat.msg import PackageInfoOut

class BaxterPackageDB:
    def __init__(self):
        self.baxter_db = baxter_database.BaxterSqlDatabase('localhost', 'root', 'root','Baxter')
        self.baxter_email = baxter_email_handler.BaxterEmail()
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("DBChannel", PackageInfoIn, callback)
        self.pub = rospy.Publsiher("DBChannel", PackageInfoOut, queue_size=10)
        rospy.init_node('talker', anonymous=True)

    def alert_listener(self):
        rospy.spin()

    def callback(self, data):
        CIDNumber = PackageInfoIn.CIDNumber
        Address = PackageInfoIn.Address
        Store = PackageInfoIn.Store
        if(Store == True):
            package_location = add_package_to_database(CIDNumber, Address)
            name = self.baxter_db.find_person_name(CIDNumber = CIDNumber)
            self.baxter_email.send_email(name, email, 1)
            name = self.baxter_db.update_notification_state(CIDNumber, package_location, 1)
        else:
            package_location = retrieve_package_from_database(CIDNumber)
        publish_location_info(package_location, Store)

    def add_package_to_database(self, CIDNumber, Address):
        package_location = self.baxter_db.add_arrived_package(CIDNumber, Address)
        return package_location

    def retrieve_package_from_database(self, CIDNumber):
        package_location = self.baxter_db.find_package_slot(CIDNumber)
        return package_location

    def publish_location_info(self, Location, Store):
        msg = PackageInfoOut()
        msg.PackageLocation = Location
        msg.Store = Store
        rospy.loginfo(msg)
        self.pub.publish(msg)

    def email_listener(self):
        mail_requests = self.baxter_email.check_for_new_mail()
        for email in mail_requests: # Iterate through all email addresses, find the number of waiting packages and send an email to each person
            number_packages = self.baxter_db.get_number_waiting_packages(email)
            name = self.baxter_db.find_person_name(email = email)
            self.baxter_email.send_email(name, email, number_packages)
        time.sleep(600)

# Create instance and run email and alert in seperate threads

baxter_package_db = BaxterPackageDB()
thread.start_new_thread(baxter_package_db.email_listener())
thread.start_new_thread(baxter_package_db.alert_listener())
