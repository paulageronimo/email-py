import os
from loguru import logger

MAX_FILE_SIZE = 2000000

SENDER_EMAIL = "paulagero182@gmail.com"
RECEIVER_EMAIL = "geronimo@tamu.edu"
CC_EMAILS = ""

MY_PASSWORD = ""

try:
   from dev_settings import *
except ImportError:
   pass

# sending the email with the specified items.
# it will contain subject and body, while files remain optional :)
def send_email(subject, body, files):
    import smtplib #SMTP Library
    from smtplib import SMTPException
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email import encoders

    sender_email = SENDER_EMAIL
    # expects a string separated by commas ',' if it is for multiple emails
    receiver_email = RECEIVER_EMAIL
    cc_emails = CC_EMAILS
    
    to_emails = receiver_email.split(',') + cc_emails.split(',')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_emails
    message["Subject"] = subject
    message["CC"] = cc_emails

    message.attach(MIMEText(body, 'html'))

    # Loop through filenames to attach them

    for filename in files:
        attach_path = filename
        if attach_path.exists() and os.path.getsize(filename) < MAX_FILE_SIZE:
            with open(os.path.join(filename), 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename = {os.path.basename (filename)}")
                message.attach(part)
        else:
            logger.warning (f"Failed to attach {attach_path.as_posix()} as the path did not exist or the file was larger than {MAX_FILE_SIZE} bytes.")

        text = message.as_string()
        
        try:
            smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpobj.ehlo()
            smtpobj.starttls()
            smtpobj.ehlo()
            smtpobj.login(sender_email, MY_PASSWORD)
            smtpobj.sendmail(sender_email, to_emails, text)
            smtpobj.close()
        except SMTPException:
            logger.exception(f"Unable to send email from {sender_email} to {','.join(to_emails)}.")




    