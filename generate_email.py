import csv #for csv files
import os #exists to get current working directory
from loguru import logger #for log statements
from pathlib import Path
from send_email import send_email

current_dir = os.getcwd() #current working directory

import re #regular expression to check if sensitive data is in email

#regular expression for a variety of phone number formats (extensions, area codes, etc)
#source:
# https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number
# https://www.regextester.com/103299
phone_number = "(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?"

#regular expression for social security number
# xxx-xx-xxxx
#https://www.geeksforgeeks.org/how-to-validate-ssn-social-security-number-using-regular-expression/
ssid = "(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}"

#regular expression for email address
#https://www.codegrepper.com/code-examples/javascript/regex+to+check+if+string+is+an+email
email = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

#regular expression for credit card number

#regular expression for bank account number

#Info on Python regex: https://www.w3schools.com/python/python_regex.asp

#Generate email
def generate_email(recieved_contents):
    #recieved contents; specific info to change
    #in this case, recieved_contents is a dicitonary
    default = "-" #default in case variables are missing or incorrect
    expected_content = dict.fromkeys(["customer_name", "product", "mssg", "amount"], default) #content expected to recieve; dicitonary
    
    for content in expected_content:
        if content in recieved_contents:
            #if there is content, add it to corresponding recieving content
            expected_content[content] = recieved_contents[content]
        else:
            #no content found. log warning message and use default parameter for that data
            logger.warning(f"The value for {content} was not passed to write failure email. Default value {default} will be used.")
    
    #once you have contents you need, get email path
    email_template_path = Path(current_dir+"/templates/email_template.html") #get the email template html from file structure
    print(email_template_path) #print path for debugging purposes
    
    #check if path exists at locaiton you defined, and its a file
    if email_template_path.exists() and email_template_path.is_file:
        with open(str(email_template_path), "r") as message:
            html = message.read().format(**expected_content) #replace stuff in brackets in html for each of content types
    else:
        #If path doesn't exist
        logger.critical("email_template_path does not exist. Dumping expected content as string into email.")
        html = f"Error: email_template_path was not set or does not exist. Dumping email content as a string:<br/>{expected_content}"
    
    return html #return html message



#print message to alert the user what type of sensitive data is in which file
def alert(file_name, data):
    print(f"{str(file_name)} contains a {data}!")

def search_emails():
    email_dir = current_dir+"/data/emails" #directory for the emails (txt files)
    #inventory_file = current_dir+"/data/contact.csv"
    
    #inventory_file = open(inventory_file, "r")
    #inventory_reader = csv.reader(inventory_file, delimiter = ",")
    
    filenames = os.listdir(email_dir) #list off the files in email directory
    for file_name in filenames:
        #open the file
        file = open(os.path.join(email_dir, file_name), "r")
        for line in file:
            #use re.search() to see if any data of that format appears in the given text
            
            #check if text contains phone number
            contains_phone_number = re.search(phone_number, line)
            if contains_phone_number:
                alert(file_name, "phone number")
                send_alert_email("Andy", "a phone number", file_name)
            contains_ssid = re.search(ssid, line)
            
            #check if text contains social security number
            if contains_ssid:
                alert(file_name, "social security number")
                send_alert_email("Andy", "a social security number", file_name)
            
            #check if text contains email
            contains_email = re.search(email, line)
            if contains_email:
                alert(file_name, "email")
                send_alert_email("Andy", "an email address", file_name)

def send_alert_email(cust_name, product, amount):
    mssg = "It is recommended that you remove this sensitive information from the file in question."
    email_contents = {
        "customer_name": cust_name,
        "product": product,
        "mssg": mssg,
        "amount": amount
    }
    
    body = generate_email(email_contents)
    send_email(body=body, subject="Warning! Sensitive data detected in your file(s)!", files = [])
                
            
            

if __name__ == "__main__":
    search_emails()