# Sensitive Data Detector
Headstarter Spring Fellowship Week 1 Project

## Main  Objective
The program in question should scan through files and issue an alert if sensitive data is detected.
The Company Scenario from Capital One introduced the idea of a “scrubbing log” which detects sensitive information in files.
The [Sample Project](https://github.com/russellelliott/Customer-Shopping-Carts) went through the process of making a Python program that sends an email to customers if they have an item in their cart that is low in stock or out of stock.

## Functionality
Combining the two resources, my program scans through files and identifies sensitive information. If any sensitive information is detected in a file, an email is sent out alerting the user about the type of sensitive information in the file and which file that information was found in.

## Program Library Information
The sample project and my program uses the library smtplib. This library uses the SMTP protocol to send emails. To use this program to send emails from a Gmail account, a setting must be changed in your Google account.
Go into your Google Account’s security settings and turn on [“Enable Less Secure Apps”](https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4N6IDE0TUlrohDkGGugp7KdT9rkm00XVjREzmsX79duDzTD_m56zDUtnIPEZAFD4yNoF7WEjJstM2gDMo9Oo59Ca3TrCQ). This will enable the program to work properly.
Note: Google will be disabling less secure app access on May 30, 2022. The program may be affected by this.

## Running the Program
To run the program, clone this repository and open it. From there, run the file `generate_email.py`. If sensitive data is detected in the files, an email will be sent for each type of sensitive data detected in each of the files. If no sensitive data is detected in a given file, no email pertaining to that file will be sent.

## Files
### generate_email.py
Parses through the files and finds sensitive information. Uses various regex expression to detect if the email contains phone numbers, email adresses, or social secutity numbers. If sensitive information of one or more of these types is found, an email is sent for every type of sensitive information found in that file.

### send_email.py
Sends each of the individual emails generated.

### .env
Contains the environment variables neccesary for the program. They are:
- `EMAIL_USER`: The email you are sending it from
- `EMAIL_PASS`: The password to the email account you are sending the emails from
- `EMAIL_RECIEVE`: The person(s) to recieve emails. Represented as a "," delimited string.
    - For multiple emails, seperate them with commas
- `EMAIL_CC`: Secondary recipients of the emails. Represented as a "," delimited string.
    - For multiple emails, seperate them with commas
    - This field is left blank in the repo, as I had no need for it in the implementation.
    - If you wish to utilize CC emails on your end, do the following:
        - modify line 13 of `send_email.py` to :`CC_EMAILS = os.environ.get("EMAIL_CC")`
        - Add email(s) in quotes to the EMAIL_CC environment varaible in the `.env` file

The `.env` file should look something like this. There should be no spaces between the varaible name, the equal sign, and the value of the varaible (all strings in quotes). The variables themselves are just normal strings. They can have spaces.

`EMAIL_USER="email@domain.com"`
`EMAIL_PASS="p@$$w0rd"`
`EMAIL_RECIEVE="another@domain.com"`
- For multiple emails: `EMAIL_RECIEVE="another@domain.com, third@domain..com, ..., etc"`

`EMAIL_CC="somebody@domain.com"`
- For multiple emails: `EMAIL_CC="somebody@domain.com, third@domain.com, ..., etc"`

### .gitignore
File that prevents files of a given type from being pushed. Used to prevent the `.env` file from being pushed onto a git repo or otherwise being visible to others. Also prevents `.DS_Store` files (appear when you open a folder in MacOS) from being pushed

### email_template.html
Email template for the emails sent out from the program. The fields in the email correspond to a varaible in the program.