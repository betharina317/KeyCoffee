# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 7/11/23
# Module file to define Modify Menu Functions


from sql_statements import *
import dearpygui.dearpygui as dpg

#
# CAN ONLY DELETE ONE WINDOW AT A TIME, NOT PARENT WINDOWS AS WELL


# ############### Modify Item Main Windows #########
def ChooseCat():
    with dpg.window(label="Cat Menu", width=600, height=300, tag="Cat Menu"):
        dpg.add_text("Select which category describes the item you want to modify,")
        dpg.add_text("or select Add Item: ")

        # Create button for each menu category in DB
        MenuCatList = SelectAllMenuCatSQL()
        for i in MenuCatList:
            dpg.add_button(label=i, user_data=i, callback=ChooseItem)

        dpg.add_button(label="Add Item", callback=AddItem)
        dpg.add_button(label="Go Back to Main", callback=lambda: dpg.delete_item("Cat Menu"))


def ChooseItem(sender, app_data, user_data):
    cat_input = user_data[0]
    itemList = SelectIDNameItem(cat_input)

    with dpg.window(label="Item Menu", width=600, height=300, tag="Item Menu"):
        dpg.add_text("Select which item you want to modify:")

        # Create button for every item under selected category
        for i in itemList:
            dpg.add_button(label=i, user_data=i, callback=DeleteOrModify)

        dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Item Menu"))


def DeleteOrModify(sender, app_data, user_data):
    itemID = int(user_data[0])

    with dpg.window(label="Delete or Modify", width=600, height=300, tag="Delete Or Modify"):
        # User chooses action to take with selected item
        dpg.add_text("Choose an option: ")
        dpg.add_button(label="Delete Item", user_data=itemID, callback=DeleteItem)
        dpg.add_button(label="Modify Item", user_data=itemID, callback=ModifyItem)
        dpg.add_button(label="Modify Item Mod Types", user_data=itemID, callback=ChooseModType)
        dpg.add_button(label="Modify Item Mods", user_data=itemID, callback=ChooseModTypeForMod)
        dpg.add_button(label="Go Back to Items", callback=lambda: dpg.delete_item("Delete Or Modify"))


# ########## Add Item Windows ############################

def AddItem():
    with dpg.window(label="New Cat Menu", width=600, height=300, tag="New Cat Menu"):
        dpg.add_text("Select which category best describes the item you want to add:")

        # Create button for each menu category in DB
        MenuCatList = SelectAllMenuCatSQL()
        for i in MenuCatList:
            dpg.add_button(label=i, user_data=i, callback=InsertItem)

        dpg.add_button(label="Go Back to Modify Menu", callback=lambda: dpg.delete_item("New Cat Menu"))


def InsertItem(sender, app_data, user_data):
    with dpg.window(label="Show Items", width=600, height=300, tag="Show Items"):
        # Show current items
        dpg.add_text("Current items in this category:")
        cat_input = user_data[0]
        itemList = SelectIDNameItem(cat_input)
        for i in itemList:
            dpg.add_text(i)

        # Add new item info
        dpg.add_text("Enter name of new item: ")
        dpg.add_input_text(tag="name_input")
        dpg.add_text("Enter price of new item: ")
        dpg.add_input_text(tag="price_input", decimal=True)
        dpg.add_button(label="Add Item", user_data=user_data, callback=InsertModType)

        dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Show Items"))


def InsertModType(sender, app_data, user_data):
    # Insert item into DB
    cat_input = user_data[0]
    name_input = dpg.get_value("name_input")
    price_input = dpg.get_value("price_input")
    newItemID = InsertItemSQL(cat_input, name_input, price_input)

    # Insert Special and Here/To Go Mods by default !!(NEEDS ERROR HANDLING)!!
    customItemTypeID = InsertItemModTypeSQL("Custom Mod", newItemID)
    hereItemTypeID = InsertItemModTypeSQL("Here/To Go", newItemID)
    InsertItemModSQL(customItemTypeID, "Custom Mod", 0)
    InsertItemModSQL(hereItemTypeID, "Here", 0)
    InsertItemModSQL(hereItemTypeID, "To Go", 0)

    with dpg.window(label="Insert Mod Type", width=600, height=300, tag="Insert Mod Type"):
        dpg.add_text("Item successfully added and new ID = " + str(newItemID))

        # Enter new mod type info
        dpg.add_text("Enter name of new Mod Type: ")
        dpg.add_input_text(tag="type_name_input")
        dpg.add_button(label="Add Mod Type", user_data=newItemID, callback=InsertMods)

        dpg.add_button(label="Go Back to Add Item", user_data=None,
                       callback=lambda: dpg.delete_item("Insert Mod Type"))


# This function called from multiple functions (re-used)
def InsertMods(sender, app_data, user_data):
    # Insert Mod Type Info into DB
    item_ID_input = user_data
    type_name_input = dpg.get_value("type_name_input")
    newModTypeID = InsertItemModTypeSQL(type_name_input, item_ID_input)

    with dpg.window(label="Insert Mods", width=600, height=300, tag="Insert Mods"):
        dpg.add_text("Mod type successfully added and new ID = " + str(newModTypeID))

        # Enter new mod info
        dpg.add_text("Enter name of new Mod: ")
        dpg.add_input_text(tag="mod_name_input")
        dpg.add_text("Enter added cost value of new Mod: ")
        dpg.add_input_text(tag="added_cost_input", decimal=True)
        dpg.add_button(label="Add Mod", user_data=newModTypeID, callback=InsertModConfirm)

        dpg.add_button(label="Go Back to Mod Type", user_data=None,
                       callback=lambda: dpg.delete_item("Insert Mods"))


# This function called from multiple functions (re-used)
def InsertModConfirm(sender, app_data, user_data):
    # Insert Mod info into DB
    type_ID_input = user_data
    mod_name_input = dpg.get_value("mod_name_input")
    added_cost_input = dpg.get_value("added_cost_input")
    newModID = InsertItemModSQL(type_ID_input, mod_name_input, added_cost_input)

    with dpg.window(label="Insert Mod Confirm", width=600, height=300, tag="Insert Mod Confirm"):
        dpg.add_text("Mod successfully added and new ID = " + str(newModID))

        dpg.add_button(label="Go Back to Add Mod", user_data=None,
                       callback=lambda: dpg.delete_item("Insert Mod Confirm"))


# ########## Delete Item Window ############################


def DeleteItem(sender, app_data, user_data):
    errMessage = DeleteItemSQL(user_data)
    itemIDList = ValidItemChoices()

    # Checks for error message deleting item
    # If none: confirms deletion
    if user_data in itemIDList:
        message = "Issue deleting item: " + str(errMessage)
    else:
        message = "Item number " + str(user_data) + " successfully deleted\n" \
                    "Unable to modify item that doesn't exist.\n" \
                    "Return to category menu to reflect changes."

    with dpg.window(label="Delete Confirm", width=600, height=300, tag="Delete Confirm"):
        dpg.add_text(message)

        dpg.add_button(label="Go Back to Modify Item Menu", callback=lambda: dpg.delete_item("Delete Confirm"))


# ########## Modify Item Windows ############################


def ModifyItem(sender, app_data, user_data):
    itemInfo = SelectNamePriceSpecifiedItem(user_data)
    with dpg.window(label="Modify Item", width=600, height=300, tag="Modify Item"):
        dpg.add_text("Current name and price of item: " + str(itemInfo))
        dpg.add_text("(Recent changes may not be reflected)\n")

        # Enter new info to update specified value in DB
        dpg.add_text("Enter new name for item: ")
        dpg.add_input_text(tag="name_input")
        dpg.add_button(label="Change Name", user_data=user_data, callback=ModifyItemName)
        dpg.add_text("Enter new price for item: ")
        dpg.add_input_text(tag="price_input", decimal=True)
        dpg.add_button(label="Change Price", user_data=user_data, callback=ModifyItemPrice)

        dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Modify Item"))


def ModifyItemName(sender, app_data, user_data):
    # Updates Item name in DB
    name_input = dpg.get_value("name_input")
    errMessage = UpdateItemName(name_input, user_data)
    newItemInfo = SelectNameSpecifiedItem(user_data)

    # Checks for error message updating item name
    # If none: confirms deletion
    if len(errMessage) == 0:
        message = newItemInfo
    else:
        message = errMessage
    with dpg.window(label="Modify Item Name", width=600, height=300, tag="Modify Item Name"):
        dpg.add_text("New name of item: " + str(message))

        dpg.add_button(label="Go Back to Modify Item", callback=lambda: dpg.delete_item("Modify Item Name"))


def ModifyItemPrice(sender, app_data, user_data):
    # Updates item price in DB
    price_input = dpg.get_value("price_input")
    errMessage = UpdateItemPrice(price_input, user_data)
    newItemInfo = SelectNamePriceSpecifiedItem(user_data)

    # Checks for error message deleting Item price
    # If none: confirms deletion
    if len(errMessage) == 0:
        message = newItemInfo
    else:
        message = errMessage
    with dpg.window(label="Modify Item Price", width=600, height=300, tag="Modify Item Price"):
        dpg.add_text("New price of item: " + str(message))

        dpg.add_button(label="Go Back to Modify Item", callback=lambda: dpg.delete_item("Modify Item Price"))


# ########## Modify Item Mod Types Windows ############################
def ChooseModType(sender, app_data, user_data):
    with dpg.window(label="Show Mod Types", width=600, height=300, tag="Show Mod Types"):
        dpg.add_text("Select which Mod Type to modify: ")

        # Create button for every mod type available in DB
        modTypeList = SelectAllSpecifiedModType(user_data)
        for i in modTypeList:
            dpg.add_button(label=i, user_data=i, callback=ModifyModType)

        # Or add new type
        dpg.add_text("Or Add new Mod Type: ")
        dpg.add_input_text(tag="type_name_input")
        dpg.add_button(label="Add New Mod Type", user_data=user_data, callback=InsertMods)

        dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Show Mod Types"))


def ModifyModType(sender, app_data, user_data):
    type_input = user_data[0]

    # Show current Mod Type info
    itemInfo = SelectNameSpecifiedModType(type_input)
    with dpg.window(label="Modify Mod Type", width=600, height=300, tag="Modify Mod Types"):
        dpg.add_text("Current name of Mod Type: " + str(itemInfo))
        dpg.add_text("(Recent changes may not be reflected)\n")

        # Offer to delete Mod Type
        dpg.add_text("Delete Mod Type: ")
        dpg.add_button(label="Delete Mod Type", user_data=type_input, callback=DeleteModType)

        # Offer to modify name of Mod Type
        dpg.add_text("Enter new name for Mod Type: ")
        dpg.add_input_text(tag="name_input")
        dpg.add_button(label="Change Name", user_data=type_input, callback=ModifyModTypeName)

        dpg.add_button(label="Go Back to Choose Mod Type", callback=lambda: dpg.delete_item("Modify Mod Types"))


def DeleteModType(sender, app_data, user_data):
    # Delete Mod Type in DB
    errMessage = DeleteModTypeSQL(user_data)
    typeIDList = ValidModTypeChoices(user_data)

    # Checks for error message deleting mod type
    # If none: confirms deletion
    if user_data in typeIDList:
        message = "Issue deleting Mod Type: " + str(errMessage)
    else:
        message = "Mod type number " + str(user_data) + " successfully deleted\n" \
                    "Unable to modify Mod Type that doesn't exist.\n" \
                    "Return to Delete or Modify Menu to reflect changes."

    with dpg.window(label="Delete Mod Type Confirm", width=600, height=300, tag="Delete Mod Type Confirm"):
        dpg.add_text(message)
        dpg.add_button(label="Go Back to Modify Mod Type", callback=lambda: dpg.delete_item("Delete Mod Type Confirm"))


def ModifyModTypeName(sender, app_data, user_data):
    # Updates Mod Type name in DB
    name_input = dpg.get_value("name_input")
    errMessage = UpdateItemModType(name_input, user_data)
    newItemInfo = SelectNameSpecifiedModType(user_data)

    # Checks for error message updating Mod Type name
    # If none: confirms update
    if len(errMessage) == 0:
        message = newItemInfo
    else:
        message = errMessage
    with dpg.window(label="Modify Mod Type", width=600, height=300, tag="Modify Mod Type"):
        dpg.add_text("New name of Mod Type: " + str(message))

        dpg.add_button(label="Go Back to Modify Mod Type", callback=lambda: dpg.delete_item("Modify Mod Type"))


# ########## Modify Item Mods Windows ############################
def ChooseModTypeForMod(sender, app_data, user_data):
    with dpg.window(label="Show Mod Types for Mods", width=600, height=300, tag="Show Mod Types for Mods"):
        dpg.add_text("Select which Mod Type Mod fits under: ")
        modTypeList = SelectAllSpecifiedModType(user_data)
        # Create button for every available mod type under specified item in DB
        for i in modTypeList:
            dpg.add_button(label=i, user_data=i, callback=ChooseMod)

        dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Show Mod Types for Mods"))


def ChooseMod(sender, app_data, user_data):
    type_input = user_data[0]
    with dpg.window(label="Show Mods", width=600, height=300, tag="Show Mods"):
        dpg.add_text("Select which Mod Type to modify: ")
        modList = SelectAllSpecifiedMod(type_input)

        # Create button for every mod available under specified mod type in DB
        for i in modList:
            dpg.add_button(label=i, user_data=i, callback=ModifyMod)

        # Offer to add new Mod
        dpg.add_text("Or Add new Mod name: ")
        dpg.add_input_text(tag="mod_name_input")
        dpg.add_text("and price: ")
        dpg.add_input_text(tag="added_cost_input")
        dpg.add_button(label="Add New Mod", user_data=type_input, callback=InsertModConfirm)

        dpg.add_button(label="Go Back to Show Mod Types", callback=lambda: dpg.delete_item("Show Mods"))


def ModifyMod(sender, app_data, user_data):
    mod_input = user_data[0]

    # Show current Mod info
    itemInfo = SelectNameCostSpecifiedMod(mod_input)
    with dpg.window(label="Modify Mod", width=600, height=300, tag="Modify Mod"):
        dpg.add_text("Current name of Mod: " + str(itemInfo))
        dpg.add_text("(Recent changes may not be reflected)\n")

        # Offer to delete Mod
        dpg.add_text("Delete Mod: ")
        dpg.add_button(label="Delete Mod", user_data=mod_input, callback=DeleteMod)

        # Offer to update Mod name or cost
        dpg.add_text("Enter new name for Mod: ")
        dpg.add_input_text(tag="change_mod_name_input")
        dpg.add_button(label="Change Name", user_data=mod_input, callback=ModifyModName)
        dpg.add_text("Enter new added cost for Mod: ")
        dpg.add_input_text(tag="change_added_cost_input")
        dpg.add_button(label="Change Added Cost", user_data=mod_input, callback=ModifyModCost)

        dpg.add_button(label="Go Back to Choose Mod", callback=lambda: dpg.delete_item("Modify Mod"))


def DeleteMod(sender, app_data, user_data):
    # Deletes Mod in DB
    errMessage = DeleteModSQL(user_data)
    modIDList = ValidModChoices(user_data)

    # Checks for error message deleting mod
    # If none: confirms deletion
    if user_data in modIDList:
        message = "Issue deleting Mod: " + str(errMessage)
    else:
        message = "Mod number " + str(user_data) + " successfully deleted\n" \
                    "Unable to modify Mod that doesn't exist.\n" \
                    "Return to Delete or Modify Menu to reflect changes."

    with dpg.window(label="Delete Mod Confirm", width=600, height=300, tag="Delete Mod Confirm"):
        dpg.add_text(message)
        dpg.add_button(label="Go Back to Modify Mod", callback=lambda: dpg.delete_item("Delete Mod Confirm"))


def ModifyModName(sender, app_data, user_data):
    # Updates Mod name in DB
    name_input = dpg.get_value("change_mod_name_input")
    errMessage = UpdateModName(name_input, user_data)
    newItemInfo = SelectNameCostSpecifiedMod(user_data)

    # Checks for error message updating Mod name
    # If none: confirms update
    if len(errMessage) == 0:
        message = newItemInfo
    else:
        message = errMessage
    with dpg.window(label="Modify Mod Name", width=600, height=300, tag="Modify Mod Name"):
        dpg.add_text("New name of Mod: " + str(message))

        dpg.add_button(label="Go Back to Modify Mod", callback=lambda: dpg.delete_item("Modify Mod Name"))


def ModifyModCost(sender, app_data, user_data):
    # Updates mod price in DB
    cost_input = dpg.get_value("change_added_cost_input")
    errMessage = UpdateModAddedCost(cost_input, user_data)
    newItemInfo = SelectNameCostSpecifiedMod(user_data)

    # Checks for error message updating Mod price
    # If none: confirms update
    if len(errMessage) == 0:
        message = newItemInfo
    else:
        message = errMessage
    with dpg.window(label="Modify Mod Cost", width=600, height=300, tag="Modify Mod Cost"):
        dpg.add_text("New cost of Mod: " + str(message))

        dpg.add_button(label="Go Back to Modify Mod", callback=lambda: dpg.delete_item("Modify Mod Cost"))