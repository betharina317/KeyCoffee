# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 6/23/23
# Module file to define Menu Function

from ModifyMenu import *
from AddOrder import *
from Reports import *
from AdminFunctions import *
import dearpygui.dearpygui as dpg


# Menu Function
def Menu():
    try:
        dpg.create_context()
        dpg.create_viewport(title='Key Coffee POS', width=600, height=400)

        with dpg.window(tag="Main Menu"):
            dpg.add_button(label="Modify Menu", user_data=ChooseCat, callback=EnterLoginWindow, tag="Modify Menu")
            dpg.add_button(label="Add Order", callback=ChooseCatOrder, tag="Add Order")
            dpg.add_button(label="Download Reports", user_data=ReportsMenu, callback=EnterLoginWindow,
                           tag="Download Reports")
            dpg.add_button(label="Add Authorized User", user_data=AddUser, callback=EnterLoginWindow,
                           tag="Add Authorized User")

        dpg.set_primary_window("Main Menu", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    except Exception as e:
        logging.debug("Error: %r", e)