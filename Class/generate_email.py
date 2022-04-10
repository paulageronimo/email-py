import csv 
import os # get the curr working dir
from loguru import logger # logger 
from pathlib import Path 

currDir = os.getcwd() # current working directory

def generate_email(received_contents): # r_c is a library
    default = "-"
    expected_content = dict.fromkeys(['customer_name', 'product', 'msg', 'amount'], default)
    for content in expected_content:
        logger.warning (f"The value for {content} was not passed to write failure email. Default value {default} will be used")

    email_template_path = Path(currDir+"templates/email_template.html")
    print(email_template_path)

    if email_template_path.exists() and email_template_path.is_file():
        with open(str(email_template_path), 'r') as message: # r to read, if write it is w
            html = message.read().format(**expected_content)
    else: # critical warning
        logger.critical("EMAIL_TEMPLATE_PATH does not exist.")
        html = f"ERROR: EMAIL_TEMPLATE_PATH was not set or does not exist so dumping email content as string:<br/>{expected_content}"

    return html

