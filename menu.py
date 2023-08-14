# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 6/23/23
# Module file to define Menu Function

from AddOrder import *
from AdminFunctions import *
import dearpygui.dearpygui as dpg


# Menu Function
def Menu():
    try:
        dpg.create_context()
        dpg.create_viewport(title='Key Coffee POS', width=600, height=400)

        with dpg.window(tag="Main Menu"):
            dpg.add_button(label="Add Order", user_data=ChooseCatOrder, callback=EnterLoginWindow, tag="Add Order")
            dpg.add_button(label="Admin Menu", user_data=VerifyOwnerAccess, callback=EnterLoginWindow, tag="Admin Menu")

        dpg.set_primary_window("Main Menu", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
    except Exception as e:
        logging.debug("Error: %r", e)