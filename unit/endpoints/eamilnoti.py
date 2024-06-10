# send email notification to the user
import smtplib
import sqlite3
from email.mime.text import MIMEText

def getSetting(name):
    conn = sqlite3.connect('sensordata.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT Svalue FROM Settings WHERE Sname = \'{name}\'')
    sVAl = cursor.fetchall()  
    conn.close()

    return sVAl[0][0]


def send(message_message, message_subject):
    sender = getSetting('sender') # senders email address
    receiver = getSetting('receiver') # recipient email address

    # email details for sender account
    smtp_server = getSetting('smtp_server')
    smtp_port = getSetting('smtp_port')
    smtp_username = getSetting('sender') # senders email address
    smtp_password = getSetting('password')

    # Build the message with MIMEText for proper formatting
    # body of the email
    message = MIMEText(message_message)
    message['Subject'] = message_subject
    message['From'] = sender
    message['To'] = receiver

    try:
        smtpObj = smtplib.SMTP(smtp_server, smtp_port)
        smtpObj.starttls()  
        
        smtpObj.login(smtp_username, smtp_password)
        
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("Successfully sent email to: ", receiver)

    except smtplib.SMTPException as e:
        print(f"Error: {e}")