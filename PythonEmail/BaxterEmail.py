import smtplib
import imaplib
import email

class Email:
    def __init__(self):
            self.gmail_user = 'PostBotPat@gmail.com'
            self.gmail_password = 'Baxter2018'

    def connect_to_smtp_server(self):
        self.smtp_server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)    # Start secure connecton to the server
        self.smtp_server_ssl.ehlo()                                       # Say Hello to the server
        self.smtp_server_ssl.login(self.gmail_user, self.gmail_password)

    def connect_to_imap_server(self):
        self.imap_server_ssl = imaplib.IMAP4_SSL('imap.gmail.com', 993)   #
        self.imap_server_ssl.login(self.gmail_user, self.gmail_password)
        self.imap_server_ssl.select('inbox')

    def get_mail_ids(self):
        type, data = self.imap_server_ssl.search(None, 'ALL')
        mail_ids = data[0]
        return mail_ids.split()


    def fetch_emails(self, id_list):
        print len(id_list)
        for i in range(int(id_list[0]), int(id_list[-1]), 1):
            type, data = self.imap_server_ssl.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print 'From : ' + email_from + '\n'
                    print 'Subject : ' + email_subject + '\n'


    def check_for_new_mail(self):
        self.connect_to_imap_server()
        self.fetch_emails(self.get_mail_ids())


email = Email()
email.check_for_new_mail()
