# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/2/23
# Module file to define password Functions

import dearpygui.dearpygui as dpg
from sql_statements import *

# #### How to delete windows in callback function with additional function???

# !!!!! filepath will need changed with new user!!!!!
filepath = r"C:\Users\Andrew\PycharmProjects\KeyCoffee\Passwords.txt"


# # Re-usable Code!!
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


# # Re-Usable Code and User Verification!!
def EnterLoginWindow(sender, app_data, user_data):
    with dpg.window(label="Enter Login Window", width=600, height=300, tag="Enter Login Window"):

        try:
            dpg.add_text("Enter Authorized PIN for Access:")
            dpg.add_input_text(tag="Pin Verification", decimal=True)
            dpg.add_button(label="Login", user_data=user_data, callback=VerifyLoginWindow)

        except Exception as e:
            logging.debug("Error: %r", e)

        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Enter Login Window"))


# # Re-Usable Code and User Verification!!
def VerifyLoginWindow(sender, app_data, user_data):
    with dpg.window(label="Verify Login Window", width=600, height=300, tag="Verify Login Window"):

        try:
            pin = dpg.get_value("Pin Verification")
            print(user_data)

            # Passes function from main menu as user_data
            if VerifyLogin(pin, filepath):
                dpg.add_text("Verified Authorization.")
                dpg.add_button(label="Continue", user_data=None, callback=user_data)
                dpg.delete_item("Enter Login Window")

            else:
                dpg.add_text("Pin Invalid.  Access Denied.")

        except Exception as e:
            logging.debug("Error: %r", e)

        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Verify Login Window"))


# #####TBD: Decide and implement authentication system
def AddUser(sender, app_data, user_data):
    with dpg.window(label="Verify Login Window", width=600, height=300, tag="Verify Login Window"):

        try:
            dpg.add_text("Enter ")

        except Exception as e:
            logging.debug("Error: %r", e)

        dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Verify Login Window"))