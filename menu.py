# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 6/23/23
# Module file to define Menu Function

from ModifyMenu import *
from AddOrder import *
import dearpygui.dearpygui as dpg


def get_value(sender):
    user_input = dpg.get_value(sender)


# Menu Function
def Menu():
    dpg.create_context()
    dpg.create_viewport(title='Key Coffee POS', width=600, height=300)

    with dpg.window(tag="Main Menu"):
        dpg.add_button(label="Modify Menu", callback=ChooseCat, tag="Modify Menu")
        dpg.add_button(label="Add Order", callback=ChooseCatOrder, tag="Add Order")

    dpg.set_primary_window("Main Menu", True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


    # user_input = int(input("\nEnter number for what you would like to do: "))

    # # Validates user input
    # while user_input not in [1, 2, 3, 4]:
    #     user_input = int(input("Please choose number 1-4:"))
    #
    # if user_input == 1:
    #     print("To be Made")
    #
    # if user_input == 2:
    #     print("Enter 1 to add Menu Item")
    #     print("Enter 2 to modify existing Menu Item")
    #     user_input = int(input())
    #
    #     # Validates user input
    #     while user_input not in [1, 2]:
    #         user_input = int(input("Please choose number 1-2:"))
    #
    #     if user_input == 1:
    #         AddItem()
    #         Menu()
    #
    #     if user_input == 2:
    #         ModifyItemMain()
    #         Menu()
    #
    # if user_input == 3:
    #     print("To be done")
    #
    # if user_input == 4:
    #     exit()