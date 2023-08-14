# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/2/23
# Module file to define password Functions

from Reports import *
from ModifyMenu import *
import dearpygui.dearpygui as dpg
import bcrypt


# ################ User Authentication Functions ##################################
# # Re-usable Code!!
def check_password(plain_text_password, hashed_password):
    try:
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)
    except Exception as e:
        logging.debug('Error: r%', e)


# # Re-Used Code and User Verification!!
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
    try:
        with dpg.window(label="Verify Login Window", width=600, height=300, tag="Verify Login Window"):
            pin = dpg.get_value("Pin Verification")
            pin = str(pin).encode('UTF-8')

            validPins = ValidLoginChoices()
            checkResult = False
            for i in validPins:
                check = check_password(pin, i)
                if check:
                    checkResult = True
                    hash = i
                else:
                    pass
            if checkResult:
                dpg.add_text("Pin Verified.")
                dpg.add_button(label="Continue", user_data=hash, callback=user_data)
                dpg.delete_item("Enter Login Window")
            else:
                dpg.add_text("Verification failed.  Please try new pin.")

            dpg.add_button(label="Go Back", callback=lambda: dpg.delete_item("Verify Login Window"))

    except Exception as e:
        logging.debug("Error: %r", e)


def VerifyOwnerAccess(sender, app_data, user_data):
    try:
        with dpg.window(label="Verify Access Window", width=600, height=300, tag="Verify Access Window"):
            dpg.delete_item("Verify Login Window")
            hash = user_data
            access = SelectHashOwnerAccess(hash)
            if isinstance(access[0][0], int):
                if access[0][0] == 1:
                    dpg.add_text("Privileged Access Verified.")
                    dpg.add_button(label="Continue", callback=AdminMenu)
                else:
                    dpg.add_text("Privileged Access Denied.")
                    dpg.add_button(label="Go Back", callback=lambda: dpg.delete_item("Verify Access Window"))
            else:
                dpg.add_text("Error selecting hash: " + access)

    except Exception as e:
        logging.debug("Error: %r", e)


def AdminMenu(sender, app_data, user_data):
    try:
        dpg.delete_item("Verify Access Window")
        with dpg.window(label="Administrator Menu", width=400, height=150, tag="Administrator Menu"):
            dpg.add_button(label="Modify Menu", callback=ChooseCat, tag="Modify Menu")
            dpg.add_button(label="Download Reports", callback=ReportsMenu, tag="Download Reports")
            dpg.add_button(label="Edit Authorized Users", callback=EditUsers, tag="Edit Authorized Users")

            dpg.add_button(label="Back to Main Menu", user_data=None,
                           callback=lambda: dpg.delete_item("Administrator Menu"))
    except Exception as e:
        logging.debug("Error: %r", e)


# ################ Edit User Functions ##################################
def get_hashed_password(pin):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    pin = str(pin).encode('UTF-8')
    return bcrypt.hashpw(pin, bcrypt.gensalt())


def EditUsers(sender, app_data, user_data):
    try:
        dpg.delete_item("Verify Login Window")
        with dpg.window(label="Edit Users", width=600, height=300, tag="Edit Users"):
            dpg.add_text("Enter Employee Name to Delete:")
            dpg.add_text("(Must delete and add new to edit)")
            dpg.add_input_text(tag="User Name")
            dpg.add_button(label="Delete", user_data=dpg.get_value("User Name"), callback=DeleteUser)
            dpg.add_text("or Add New User:")
            dpg.add_button(label="Add User", callback=EnterNewUser)

            dpg.add_button(label="Back to Admin Menu", callback=lambda: dpg.delete_item("Edit Users"))

    except Exception as e:
        logging.debug("Error: %r", e)


def DeleteUser(sender, app_data, user_data):
    try:
        with dpg.window(label="Delete User", width=600, height=300, tag="Delete User"):
            name = user_data
            nameList = ValidLoginNameChoices()
            if name in nameList:
                result = DeleteLoginSQL(name)
                if len(result) == 0:
                    message = "User successfully deleted!"
                else:
                    message = result
            else:
                message = "User not in User Table.  Unable to Delete."
            dpg.add_text(message)
            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Delete User"))

    except Exception as e:
        logging.debug("Error: %r", e)


def EnterNewUser(sender, app_data, user_data):
    try:
        with dpg.window(label="Enter User", width=600, height=300, tag="Enter User"):

            dpg.add_text("Enter New Employee Name:")
            dpg.add_input_text(tag="New Name")
            dpg.add_radio_button(tag="Access", items=['Basic Access', 'Advanced Access'],
                                 default_value='Basic Access', horizontal=True)
            dpg.add_text("Enter New PIN:")
            dpg.add_input_text(tag="New Pin", decimal=True)
            dpg.add_text("Confirm New PIN:")
            dpg.add_input_text(tag="Confirm New Pin", decimal=True)
            dpg.add_button(label="Enter", callback=AddNewUser)

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Enter User"))
    except Exception as e:
        logging.debug("Error: %r", e)


def AddNewUser(sender, app_data, user_data):
    try:
        name = dpg.get_value("New Name")
        ownerAccess = dpg.get_value("Access")
        pin = dpg.get_value("New Pin")
        confPin = dpg.get_value("Confirm New Pin")
        print(name,ownerAccess,pin,confPin)

        if pin != confPin:
            with dpg.window(label="Not Matching pin", width=600, height=300, tag="Not Matching pin"):
                dpg.add_text("Pins do not match.  Please try again.")
                dpg.add_button(label="Go back", callback=lambda: dpg.delete_item("Not Matching pin"))
        elif len(pin) != 4:
            with dpg.window(label="Bad pin", width=600, height=300, tag="Bad pin"):
                dpg.add_text("Pin needs to be 4 numbers.  Please try again")
                dpg.add_button(label="Go back", callback=lambda: dpg.delete_item("Bad pin"))
        elif ownerAccess == 'Basic Access':
            ownerAccess = 0
        else:
            ownerAccess = 1
        # Encode/hash username if other than emp
        hash = get_hashed_password(pin)

        result = InsertLogin(name, hash, ownerAccess)
        with dpg.window(label="User Added", width=600, height=300, tag="User Added"):
            dpg.add_text("User added successfully!  New ID = " + str(result))
            dpg.delete_item("Enter User")

            dpg.add_button(label="Go back to Edit Users", callback=lambda: dpg.delete_item("User Added"))

    except Exception as e:
        logging.debug("Error: %r", e)

