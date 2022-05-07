import os
from loguru import logger

from dotenv import load_dotenv
load_dotenv() #take environment variables from .env

MAX_FILE_SIZE = 2000000 #maximum size of file

#get email and password from .env files for security purposes
SENDER_EMAIL = os.environ.get("EMAIL_USER")
MY_PASSWORD = os.environ.get("EMAIL_PASS")
RECIEVER_EMAIL = os.environ.get("EMAIL_RECIEVE")
CC_EMAILS = "" #os.environ.get("EMAIL_CC")

#Send email with specific subject, message, and files as attatchements being optional
def send_email(subject, body, files):
    import smtplib
    from smtplib import SMTPException
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email import encoders
    
    sender_email = SENDER_EMAIL
    
    #expecting a string of "," delimited emails
    reciever_email = RECIEVER_EMAIL
    cc_emails = CC_EMAILS
    
    to_emails = reciever_email.split(",") + cc_emails.split(",")
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciever_email
    message["Subject"] = subject
    message["CC"] = cc_emails
    
    message.attach(MIMEText(body, "html")) #define body as html
    
    #Loop through filenames to attatch files passed through
    for filename in files:
        attach_path = filename
        #check if file path exists, and file is within size contraints
        if attach_path.exists() and os.path.getsize(filename) < MAX_FILE_SIZE:
            with open(os.path.join(filename), "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Dispositon",
                    f"attachement; filename = {os.path.basename(filename)}",
                )
                message.attach(part)
        else:
            #if file DNE or file is too large, issue warning of failure to attach
            logger.warning(f"Failed to attach {attach_path.as_posix()} as the path did not exist or the file was larger than {MAX_FILE_SIZE} bytes.")
    
    text = message.as_string()
    
    try:
        smtpobj = smtplib.SMTP("smtp.gmail.com", 587) #define smtp instance for gmail. use the port number 587
        smtpobj.ehlo()
        smtpobj.starttls() #start session
        smtpobj.ehlo()
        smtpobj.login(sender_email, MY_PASSWORD) #login to the email account to send the email
        smtpobj.sendmail(sender_email, to_emails, text) #send the email
        smtpobj.close() #close session
    except SMTPException:
        logger.exception(f"Unable to send email. Failed to send from {sender_email} to {to_emails}.")