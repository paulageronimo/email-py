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

def search_customer_lists():
    customer_dir = currDir+"/CSV material generator/customer_carts"
    inventory_file = currDir+"/CSV_material_generator/inventory_items.csv"
    low_stock = {}
    no_stock = {}
    inventory_file = open(inventory_file, "r")
    inventory_reader = csv.reader(inventory_file, delimiter=',')
    for row in inventory_reader:
        if "Amount" in row[1]:
            continue
        elif int(row[1]) == 0:
            no_stock[row[0]] = row[1]
        elif int(row[1]) <=15:
            low_stock[row[0]] = row[1]

    filenames=os.listdir(customer_dir)

    for file_name in filenames:
        if file_name.endswith(".csv"):
            file = open(os.path. join(customer_dir, file_name),'r')
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                print (row)
                if row[0] in no_stock:
                    send_no_stock_email("Andy", row[0], no_stock[row[0]])
                elif row[0] in low_stock:
                    send_low_stock_email("Andy", row[0], low_stock[row[0]])

