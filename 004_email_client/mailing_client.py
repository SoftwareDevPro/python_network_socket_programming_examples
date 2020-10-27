
import smtplib

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Parameters for the email server
SERVER_URL  = 'smtp.live.com'
SERVER_PORT = 587

# Create the SMTP object, send extended HELO, and start TLS mode security
server = smtplib.SMTP(SERVER_URL, SERVER_PORT)
#server.set_debuglevel(1)
server.ehlo()
server.starttls()

# Read in the password, and login
with open('password.txt', 'r') as f:
    password = f.read()

server.login('jaysmith@gmail.com', password)

# Setup the message parts
msg = MIMEMultipart()
msg['From'] = 'Emmanuel Goldstein'
msg['To'] = 'joesmith@live.com'
msg['Subject'] = 'Email Test Send'

# Read in the message textual data, and attach it
with open('message.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

# Attach a file to the message
filename = 'code.jpg'
attachment = open(filename, 'rb')

payload = MIMEBase('application', 'octet-stream')
payload.set_payload(attachment.read())

encoders.encode_base64(payload)
payload.add_header('Content-Disposition', f'attachment; filename={filename}')

msg.attach(payload)

# Convert the whole message to a string, ands send it.
text = msg.as_string()

server.sendmail('joesmith@live.com', 'jaysmith@gmail.com', text)
