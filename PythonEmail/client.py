import smtplib, email.utils
from email.mime.text import MIMEText

# Create the Message
msg = MIMEText('This is the body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'owen.harcombe@gmail.com'))
msg['From'] = email.utils.formataddr(('Author', 'baxter@mailroom.com'))
msg['Subject'] = 'Parcel Ready'

server = smtplib.SMTP('localhost', 1025)
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('baxter@mailroom.com', ['owen.harcombe@gmail.com'], msg.as_string())
finally:
    server.quit()
