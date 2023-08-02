# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/2/23
# Module file to define password Functions

import dearpygui as dpg
from sql_statements import *

filepath = r"C:\Users\Andrew\PycharmProjects\KeyCoffee\Passwords.txt"


def VerifyLogin(pin, filepath):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            # Checks each line for matching pin
            for line in lines:
                if line == pin:
                    return True
        file.close()
    except Exception as e:
        print(type(Exception))
        logging.debug('Error: r%', e)

    return False


def VerifyLoginWindow():
    with dpg.window(label="Verify Login Window", width=600, height=300, tag="Verify Login Window"):

        try:
            dpg.add_
        except Exception as e:
            logging.debug("Error: %r", e)

        dpg.add_button(label="Go Back to Modify Menu", callback=lambda: dpg.delete_item("Verify Login Window"))