from menu import *
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

from PasswordFunctions import *

pin = "1235"


print(VerifyLogin(pin, filepath))
# Main
# Menu()

# # dpg demo
# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=600, height=600)
#
# demo.show_demo()
#
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

