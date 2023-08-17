# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/16/23
# Module file to define Modify Menu Functions

from sql_statements import *
import dearpygui.dearpygui as dpg


# ############### Modify Item Main Windows #########
def ChooseCat():
    try:
        with dpg.window(label="Cat Menu", width=600, height=300, tag="Cat Menu"):
            dpg.delete_item("Verify Pin Window")

            dpg.add_text("Select which category describes the item you want to modify,")
            dpg.add_text("or select Add Item: ")

            # Create button for each menu category in DB
            MenuCatList = SelectAllMenuCatSQL()
            for categoryIDName in MenuCatList:
                catID = categoryIDName[0]
                catName = categoryIDName[1]
                dpg.add_button(label=catName, user_data=catID, callback=ChooseItem)
            dpg.add_button(label="Add Item", callback=AddItem)

            dpg.add_button(label="Go Back to Admin Menu", callback=lambda: dpg.delete_item("Cat Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ChooseItem(sender, app_data, user_data):

    try:
        # Assign chosen category to variable and make list of items under category in DB
        catInput = user_data
        itemList = SelectIDNameItem(catInput)

        with dpg.window(label="Item Menu", width=600, height=300, tag="Item Menu"):
            dpg.add_text("Select which item you want to modify:")

            # Create button for every item under selected category
            for itemIDName in itemList:
                itemID = itemIDName[0]
                itemName = itemIDName[1]
                dpg.add_button(label=itemName, user_data=itemID, callback=DeleteOrModify)

            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Item Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def DeleteOrModify(sender, app_data, user_data):
    try:
        # Assign chosen item to variable
        itemID = int(user_data)

        with dpg.window(label="Delete or Modify", width=600, height=300, tag="Delete Or Modify"):
            dpg.delete_item("Item Menu")

            # User chooses action to take with selected item
            dpg.add_text("Choose an option: ")
            dpg.add_button(label="Delete Item", user_data=itemID, callback=DeleteItem)
            dpg.add_button(label="Modify Item", user_data=itemID, callback=ModifyItem)
            dpg.add_button(label="Modify Item Mod Types", user_data=itemID, callback=ChooseModType)
            dpg.add_button(label="Modify Item Mods", user_data=itemID, callback=ChooseModTypeForMod)
            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Delete Or Modify"))

    except Exception as e:
        logging.debug("Error: %r", e)


# ########## Add Item Windows ############################

def AddItem():
    try:
        with dpg.window(label="New Cat Menu", width=600, height=300, tag="New Cat Menu"):
            dpg.add_text("Select which category best describes the item you want to add:")

            # Create button for each menu category in DB
            MenuCatList = SelectAllMenuCatSQL()
            for categoryIDName in MenuCatList:
                catID = categoryIDName[0]
                catName = categoryIDName[1]
                dpg.add_button(label=catName, user_data=catID, callback=InsertItem)

            dpg.add_button(label="Go Back to Modify Menu", callback=lambda: dpg.delete_item("New Cat Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def InsertItem(sender, app_data, user_data):
    try:
        with dpg.window(label="Show Items", width=600, height=300, tag="Show Items"):
            dpg.delete_item("New Cat Menu")

            # Assign category choice to variable and create list of items under category
            catInput = user_data
            itemList = SelectIDNameItem(catInput)

            # Show current items
            dpg.add_text("Current items in this category:")
            for itemIDName in itemList:
                itemName = itemIDName[1]
                dpg.add_text(itemName)

            # Add new item info
            dpg.add_text("Enter name of new item: ")
            dpg.add_input_text(tag="name input")
            dpg.add_text("Enter price of new item: ")
            dpg.add_input_text(tag="price input", decimal=True)
            dpg.add_button(label="Add Item", user_data=catInput, callback=InsertModType)

            dpg.add_button(label="Go Back to Modify Menu", callback=lambda: dpg.delete_item("Show Items"))

    except Exception as e:
        logging.debug("Error: %r", e)


def InsertModType(sender, app_data, user_data):
    try:
        # Insert item into DB
        catInput = user_data
        nameInput = dpg.get_value("name input")
        priceInput = dpg.get_value("price input")
        newItemID = InsertItemSQL(catInput, nameInput, priceInput)

        # Insert Here/To Go Mods by default
        hereItemTypeID = InsertItemModTypeSQL("Here/To Go", newItemID)
        InsertItemModSQL(hereItemTypeID, "Here", 0)
        InsertItemModSQL(hereItemTypeID, "To Go", 0)

        with dpg.window(label="Insert Mod Type", width=600, height=300, tag="Insert Mod Type"):
            dpg.delete_item("Show Items")

            dpg.add_text("Item successfully added and new ID = " + str(newItemID))

            # Enter new mod type info
            dpg.add_text("Enter name of new Mod Type: ")
            dpg.add_input_text(tag="type name input")
            dpg.add_button(label="Add Mod Type", user_data=newItemID, callback=InsertMods)

            dpg.add_button(label="Go Back to Modify Menu", user_data=None,
                           callback=lambda: dpg.delete_item("Insert Mod Type"))

    except Exception as e:
        logging.debug("Error: %r", e)


# This function called from 2 functions (re-used)
def InsertMods(sender, app_data, user_data):
    try:
        # Insert Mod Type Info into DB
        itemIDInput = user_data
        typeNameInput = dpg.get_value("type name input")
        newModTypeID = InsertItemModTypeSQL(typeNameInput, itemIDInput)

        with dpg.window(label="Insert Mods", width=600, height=300, tag="Insert Mods"):
            dpg.add_text("Mod type successfully added and new ID = " + str(newModTypeID))

            # Enter new mod info
            dpg.add_text("Enter name of new Mod: ")
            dpg.add_input_text(tag="mod name input")
            dpg.add_text("Enter added cost value of new Mod: ")
            dpg.add_input_text(tag="added cost input", decimal=True)
            dpg.add_button(label="Add Mod", user_data=newModTypeID, callback=InsertModConfirm)

            dpg.add_button(label="Go Back to Mod Type", user_data=None,
                           callback=lambda: dpg.delete_item("Insert Mods"))

    except Exception as e:
        logging.debug("Error: %r", e)


# This function called from 2 functions (re-used)
def InsertModConfirm(sender, app_data, user_data):
    try:
        # Insert Mod info into DB
        typeIDInput = user_data
        modNameInput = dpg.get_value("mod name input")
        addedCostInput = dpg.get_value("added cost input")
        newModID = InsertItemModSQL(typeIDInput, modNameInput, addedCostInput)

        with dpg.window(label="Insert Mod Confirm", width=600, height=300, tag="Insert Mod Confirm"):
            dpg.add_text("Mod successfully added and new ID = " + str(newModID))

            dpg.add_button(label="Go Back to Add Mod", callback=lambda: dpg.delete_item("Insert Mod Confirm"))

    except Exception as e:
        logging.debug("Error: %r", e)


# ########## Delete Item Window ############################


def DeleteItem(sender, app_data, user_data):
    try:
        itemID = user_data
        # Potential error message stored in variable after deleting item
        errMessage = DeleteItemSQL(itemID)
        # Make list of item IDs in table after deletion
        itemIDList = ValidItemChoices()

        # Checks for error message deleting item. If none, confirms deletion
        if itemID in itemIDList:
            message = "Issue deleting item: " + str(errMessage)
        else:
            message = "Item number " + str(itemID) + " successfully deleted\n" \

        with dpg.window(label="Delete Confirm", width=600, height=300, tag="Delete Confirm"):
            dpg.delete_item("Delete Or Modify")

            dpg.add_text(message)

            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Delete Confirm"))

    except Exception as e:
        logging.debug("Error: %r", e)


# ########## Modify Item Windows ############################


def ModifyItem(sender, app_data, user_data):
    try:
        itemID = user_data
        # Assign item info to variable
        itemInfo = SelectNamePriceSpecifiedItem(itemID)

        with dpg.window(label="Modify Item", width=600, height=300, tag="Modify Item"):
            dpg.delete_item("Delete Or Modify")

            #Show current item info
            dpg.add_text("Current name and price of item: " + str(itemInfo))

            # Enter new info to update specified value in DB
            dpg.add_text("Enter new name for item: ")
            dpg.add_input_text(tag="name input")
            dpg.add_button(label="Change Name", user_data=itemID, callback=ModifyItemName)
            dpg.add_text("Enter new price for item: ")
            dpg.add_input_text(tag="price input", decimal=True)
            dpg.add_button(label="Change Price", user_data=itemID, callback=ModifyItemPrice)

            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Modify Item"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyItemName(sender, app_data, user_data):
    try:
        itemID = user_data
        # Updates Item name in DB and gets updated info
        nameInput = dpg.get_value("name input")
        errMessage = UpdateItemName(nameInput, itemID)
        newItemInfo = SelectNameSpecifiedItem(itemID)

        with dpg.window(label="Modify Item Name", width=600, height=300, tag="Modify Item Name"):
            dpg.delete_item("Modify Item")

            # Checks for error message updating item name
            # If none: confirms deletion
            if len(errMessage) == 0:
                message = newItemInfo
            else:
                message = errMessage

            dpg.add_text("New name of item: " + str(message))

            dpg.add_button(label="Go Back to Modify Item", callback=lambda: dpg.delete_item("Modify Item Name"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyItemPrice(sender, app_data, user_data):
    try:
        itemID = user_data
        # Updates item price in DB and gets updated info
        priceInput = dpg.get_value("price input")
        errMessage = UpdateItemPrice(priceInput, itemID)
        newItemInfo = SelectNamePriceSpecifiedItem(itemID)

        with dpg.window(label="Modify Item Price", width=600, height=300, tag="Modify Item Price"):
            dpg.delete_item("Modify Item")

            # Checks for error message deleting Item price
            # If none: confirms deletion
            if len(errMessage) == 0:
                message = newItemInfo
            else:
                message = errMessage

            dpg.add_text("New price of item: " + str(message))

            dpg.add_button(label="Go Back to Modify Item", callback=lambda: dpg.delete_item("Modify Item Price"))

    except Exception as e:
        logging.debug("Error: %r", e)


# ########## Modify Item Mod Types Windows ############################
def ChooseModType(sender, app_data, user_data):
    try:
        itemID = user_data
        with dpg.window(label="Show Mod Types", width=600, height=300, tag="Show Mod Types"):
            dpg.add_text("Select which Mod Type to modify: ")

            # Create button for every mod type available in DB
            modTypeList = SelectAllSpecifiedModType(itemID)
            for modTypeIDName in modTypeList:
                modTypeID = modTypeIDName[0]
                modTypeName = modTypeIDName[1]
                dpg.add_button(label=modTypeName, user_data=modTypeID, callback=ModifyModType)

            # Or add new type
            dpg.add_text("Or Add new Mod Type: ")
            dpg.add_input_text(tag="type name input")
            dpg.add_button(label="Add New Mod Type", user_data=itemID, callback=InsertMods)

            dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Show Mod Types"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyModType(sender, app_data, user_data):
    try:
        # Assign modTypeID to variable and obtain current Mod Type info
        typeInput = user_data
        itemInfo = SelectNameSpecifiedModType(typeInput)

        with dpg.window(label="Modify Mod Type", width=600, height=300, tag="Modify Mod Type"):
            dpg.delete_item("Show Mod Types")

            # Show current mod type input
            dpg.add_text("Current name of Mod Type: " + str(itemInfo))

            # Offer to delete Mod Type
            dpg.add_text("Delete Mod Type: ")
            dpg.add_button(label="Delete Mod Type", user_data=typeInput, callback=DeleteModType)

            # Offer to modify name of Mod Type
            dpg.add_text("Enter new name for Mod Type: ")
            dpg.add_input_text(tag="name input")
            dpg.add_button(label="Change Name", user_data=typeInput, callback=ModifyModTypeName)

            dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Modify Mod Type"))

    except Exception as e:
        logging.debug("Error: %r", e)


def DeleteModType(sender, app_data, user_data):
    try:
        typeInput = user_data
        # Delete Mod Type in DB and get current modTypeIDs in table after
        errMessage = DeleteModTypeSQL(typeInput)
        typeIDList = ValidModTypeChoices(typeInput)

        # Checks for error message deleting mod type.  If none, confirms deletion
        if typeInput in typeIDList:
            message = "Issue deleting Mod Type: " + str(errMessage)
        else:
            message = "Mod type number " + str(typeInput) + " successfully deleted\n" \

        with dpg.window(label="Delete Mod Type Confirm", width=600, height=300, tag="Delete Mod Type Confirm"):
            dpg.delete_item("Modify Mod Type")
            dpg.delete_item("Show Mod Types")

            dpg.add_text(message)

            dpg.add_button(label="Go Back to Delete or Modify",
                           callback=lambda: dpg.delete_item("Delete Mod Type Confirm"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyModTypeName(sender, app_data, user_data):
    try:
        typeInput = user_data
        # Updates Mod Type name in DB
        nameInput = dpg.get_value("name input")
        errMessage = UpdateItemModType(nameInput, typeInput)
        newItemInfo = SelectNameSpecifiedModType(typeInput)

        with dpg.window(label="Modify Mod Type", width=600, height=300, tag="Modify Mod Type"):
            dpg.delete_item("Modify Mod Type")

            # Checks for error message updating Mod Type name.  If none, confirms update
            if len(errMessage) == 0:
                message = newItemInfo
            else:
                message = errMessage

            dpg.add_text("New name of Mod Type: " + str(message))

            dpg.add_button(label="Go Back to Delete or Modify", callback=lambda: dpg.delete_item("Modify Mod Type"))

    except Exception as e:
        logging.debug("Error: %r", e)


# ########## Modify Item Mods Windows ############################
def ChooseModTypeForMod(sender, app_data, user_data):
    try:
        itemInput = user_data
        # Create list of mod types available under item ID in DB
        modTypeList = SelectAllSpecifiedModType(itemInput)

        with dpg.window(label="Show Mod Types for Mods", width=600, height=300, tag="Show Mod Types for Mods"):
            dpg.add_text("Select which Mod Type Mod fits under: ")

            # Create button for every available mod type under specified item in DB
            for modTypeIDName in modTypeList:
                modTypeID = modTypeIDName[0]
                modTypeName = modTypeIDName[1]
                dpg.add_button(label=modTypeName, user_data=modTypeID, callback=ChooseMod)

            dpg.add_button(label="Go Back to Delete or Modify",
                           callback=lambda: dpg.delete_item("Show Mod Types for Mods"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ChooseMod(sender, app_data, user_data):
    try:
        # Assigns chosen ModTypeID to variable and creates list of mods under mod type
        typeInput = user_data
        modList = SelectAllSpecifiedMod(typeInput)

        with dpg.window(label="Show Mods", width=600, height=300, tag="Show Mods"):
            dpg.add_text("Select which Mod Type to modify: ")

            # Create button for every mod available under specified mod type in DB
            for modIDName in modList:
                modID = modIDName[0]
                modName = modIDName[1]
                dpg.add_button(label=modName, user_data=modID, callback=ModifyMod)

            # Offer to add new Mod
            dpg.add_text("Or Add new Mod name: ")
            dpg.add_input_text(tag="mod name input")
            dpg.add_text("and price: ")
            dpg.add_input_text(tag="added cost input")
            dpg.add_button(label="Add New Mod", user_data=typeInput, callback=InsertModConfirm)

            dpg.add_button(label="Go Back to Show Mod Types", callback=lambda: dpg.delete_item("Show Mods"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyMod(sender, app_data, user_data):
    try:
        # Assigns chosen ModID to variable and creates list of info under ModID
        modInput = user_data
        itemInfo = SelectNameCostSpecifiedMod(modInput)

        with dpg.window(label="Modify Mod", width=600, height=300, tag="Modify Mod"):
            dpg.add_text("Current name of Mod: " + str(itemInfo))

            # Offer to delete Mod
            dpg.add_text("Delete Mod: ")
            dpg.add_button(label="Delete Mod", user_data=modInput, callback=DeleteMod)

            # Offer to update Mod name or cost
            dpg.add_text("Enter new name for Mod: ")
            dpg.add_input_text(tag="change mod name input")
            dpg.add_button(label="Change Name", user_data=modInput, callback=ModifyModName)
            dpg.add_text("Enter new added cost for Mod: ")
            dpg.add_input_text(tag="change added cost input")
            dpg.add_button(label="Change Added Cost", user_data=modInput, callback=ModifyModCost)

            dpg.add_button(label="Go Back to Choose Mod", callback=lambda: dpg.delete_item("Modify Mod"))

    except Exception as e:
        logging.debug("Error: %r", e)


def DeleteMod(sender, app_data, user_data):
    try:
        modID = user_data
        # Deletes Mod in DB
        errMessage = DeleteModSQL(modID)
        modIDList = ValidModChoices(modID)

        # Checks for error message deleting mod. If none, confirms deletion
        if modID in modIDList:
            message = "Issue deleting Mod: " + str(errMessage)
        else:
            message = "Mod number " + str(modID) + " successfully deleted"
            dpg.delete_item("Modify Mod")
            dpg.delete_item("Show Mods")

        with dpg.window(label="Delete Mod Confirm", width=600, height=300, tag="Delete Mod Confirm"):
            dpg.add_text(message)

            dpg.add_button(label="Go Back to Show Mod Types", callback=lambda: dpg.delete_item("Delete Mod Confirm"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyModName(sender, app_data, user_data):
    try:
        modID = user_data
        # Updates Mod name in DB
        nameInput = dpg.get_value("change mod name input")
        errMessage = UpdateModName(nameInput, modID)
        newItemInfo = SelectNameCostSpecifiedMod(modID)

        # Checks for error message updating Mod name. If none, confirms update
        if len(errMessage) == 0:
            message = newItemInfo
        else:
            message = errMessage

        with dpg.window(label="Modify Mod Name", width=600, height=300, tag="Modify Mod Name"):
            dpg.add_text("New name of Mod: " + str(message))

            dpg.add_button(label="Go Back to Modify Mod", callback=lambda: dpg.delete_item("Modify Mod Name"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ModifyModCost(sender, app_data, user_data):
    try:
        modID = user_data
        # Updates mod price in DB
        costInput = dpg.get_value("change added cost input")
        errMessage = UpdateModAddedCost(costInput, modID)
        newItemInfo = SelectNameCostSpecifiedMod(modID)

        # Checks for error message updating Mod price. If none, confirms update
        if len(errMessage) == 0:
            message = newItemInfo
        else:
            message = errMessage

        with dpg.window(label="Modify Mod Cost", width=600, height=300, tag="Modify Mod Cost"):
            dpg.add_text("New cost of Mod: " + str(message))

            dpg.add_button(label="Go Back to Modify Mod", callback=lambda: dpg.delete_item("Modify Mod Cost"))

    except Exception as e:
        logging.debug("Error: %r", e)