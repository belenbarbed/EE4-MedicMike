import smtplib
import imaplib
import email
import time
import re
import database_handler

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailHandler:
    def __init__(self):
        self.gmail_user = 'medicmike6969@gmail.com'
        self.gmail_password = 'Baxter2018'

    def __connect_to_smtp_server(self):
        self.smtp_server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)    # Start secure connecton to the server
        self.smtp_server_ssl.ehlo()                                       # Say Hello to the server
        self.smtp_server_ssl.login(self.gmail_user, self.gmail_password)

    def __connect_to_imap_server(self):
        self.imap_server_ssl = imaplib.IMAP4_SSL('imap.gmail.com', 993)   #
        self.imap_server_ssl.login(self.gmail_user, self.gmail_password)
        self.imap_server_ssl.select('inbox')

    def __get_mail_ids(self):
        type, data = self.imap_server_ssl.search(None, '(UNSEEN)')
        mail_ids = data[0]
        return mail_ids.split()

    def __fetch_emails(self, id_list):
        new_requests = []
        if(len(id_list) > 0):
            for i in range(int(id_list[0]), int(id_list[-1]) + 1, 1):
                type, data = self.imap_server_ssl.fetch(i, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        if(msg.is_multipart()):
                            payload = msg.get_payload()[0]
                        else:
                            payload= msg.get_payload()
                        prescription_information = re.findall(r"Patient NHS Number: ?([0-9]+)[\n\r]*Medicine Name: ?([a-zA-Z]+)[\n\r]*Dose: ?([0-9]+[a-z]*)[\n\r]*Times Per Day: ?([0-9]+)[\n\r]*Start Date: ?([0-9]{4}-[0-9]{2}-[0-9]{2})[\n\r]*Duration: ?([0-9]+)[\n\r]*Repeat Prescription\(Y\/N\): ?([YyNn]{1})", response_part[1])
                        doctor_email = re.findall(r"<(.*?)>", msg['from'])
                        prescription_information.insert(0, doctor_email[0])
                        print(prescription_information)
                        new_requests.append(prescription_information)
                self.imap_server_ssl.store(i,'+FLAGS', '\Seen')
        return new_requests

    def check_for_new_mail(self):
        self.__connect_to_imap_server()
        new_requests = self.__fetch_emails(self.__get_mail_ids())
        print new_requests
        self.imap_server_ssl.close()
        self.imap_server_ssl.logout()
        return new_requests

    def send_email(self, name, email, number_packages):
        self.__connect_to_smtp_server()
        msg = MIMEMultipart()
        print(email)
        msg['From'] = self.gmail_user
        msg['To'] = email
        msg['Subject'] = "Prescriptions ready for collection"
        body = """
        To %s,

        Medicines prescribed to you are now in stock.

        Best wishes,
        Medic Mike
        """ %(name, number_packages,)

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        self.smtp_server_ssl.sendmail(self.gmail_user, email, text)
        time.sleep(1)
        self.smtp_server_ssl.quit()
