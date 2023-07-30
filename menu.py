# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 6/23/23
# Module file to define Menu Function

from ModifyMenu import *
from AddOrder import *
from Reports import *
import dearpygui.dearpygui as dpg


# Menu Function
def Menu():
    dpg.create_context()
    dpg.create_viewport(title='Key Coffee POS', width=600, height=400)

    with dpg.window(tag="Main Menu"):
        dpg.add_button(label="Modify Menu", callback=ChooseCat, tag="Modify Menu")
        dpg.add_button(label="Add Order", callback=ChooseCatOrder, tag="Add Order")
        dpg.add_button(label="Download Reports", callback=ReportsMenu, tag="Download Reports")

    dpg.set_primary_window("Main Menu", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()