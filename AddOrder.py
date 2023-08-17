# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/16/23
# Module file to define Add Order Functions

from sql_statements import *
import dearpygui.dearpygui as dpg

# list of dicts
orderedItemMods = []
orderedItemPrice = []

# list of ints
tempModsList = []
tempCostList = []
customModsList = []


def ChooseCatOrder():
    try:
        with dpg.window(label="Cat Menu", width=600, height=300, tag="Cat Menu"):
            dpg.delete_item("Verify Login Window")
            dpg.add_text("Select which category describes the item to order:")

            # Create button for each menu category in DB
            MenuCatList = SelectAllMenuCatSQL()
            for category in MenuCatList:
                dpg.add_button(label=category, user_data=category, callback=ChooseItemOrder)

            dpg.add_button(label="Go Back to Main", callback=lambda: dpg.delete_item("Cat Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ChooseItemOrder(sender, app_data, user_data):
    try:
        # Create list of items given the category ID
        catInput = user_data[0]
        itemList = SelectAllItem(catInput)

        with dpg.window(label="Item Menu", width=600, height=300, tag="Item Menu"):
            dpg.add_text("Select which item you want to order:")

            # Create button for every item under selected category
            for item in itemList:
                dpg.add_button(label=item, user_data=item, callback=ChooseModOrder)

            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Item Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def ChooseModOrder(sender, app_data, user_data):
    try:
        # Assign Item ID to variable
        itemInput = user_data[0]
        # Append cost of item to tempCostList
        cost = user_data[2]
        tempCostList.append(cost)
        # Create list of tuples for mod types given item ID. Format: [(ID,Name),(ID,Name)]
        modTypeList = SelectAllSpecifiedModType(itemInput)

        with dpg.window(label="Mod Menu", width=600, height=300, tag="Mod Menu"):
            dpg.delete_item("Item Menu")
            dpg.add_text("Select modifications for item:")

            # Create listbox for every mod type containing mods under selected item
            for modType in modTypeList:
                modTypeID = modType[0]
                modTypeName = modType[1]
                # tempModList format: [(ID, Name, AddedCost), (ID, Name, AddedCost)]
                tempModList = SelectAllSpecifiedMod(modTypeID)
                modList = []
                for modInfo in tempModList:
                    modName = modInfo[1]
                    modList.append(modName)
                dpg.add_listbox(label=modTypeName, items=modList, user_data=modTypeID, callback=AddMod)

            dpg.add_text("or add special instructions:")
            dpg.add_input_text(label="Custom Mod", tag="Custom Mod")
            dpg.add_button(label="Add Custom Mod", callback=AddCustomMod)

            dpg.add_button(label="Add Item to Order", user_data=itemInput, callback=AddItemToOrder)
            dpg.add_button(label="Order Complete", callback=CompleteOrder)
            dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Mod Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


def AddMod(sender, app_data, user_data):
    try:
        modTypeID = user_data
        modName = dpg.get_value(sender)
        modInfo = SelectModIDSpecifiedNameModTypeID(modName, modTypeID)

        # checks for SQL error
        if isinstance(modInfo, str):
            raise Exception
        else:
            modID = modInfo[0][0]
            modCost = modInfo[0][1]

        # Adds mod to orderedItem Dict
        tempModsList.append(modID)

        # Adds AddedCost to tempCostList
        tempCostList.append(float(modCost))

    except Exception as e:
        logging.debug("Error: %r", e)


def AddCustomMod(sender, app_data, user_data):
    try:
        # Get custom mod value
        description = dpg.get_value("Custom Mod")

        # Add Custom Mod to table (if not exists)
        testCustomModIDExists = SelectExistingCustomMod(description)
        if not testCustomModIDExists:
            CustomModID = InsertCustomModSQL(description)
        else:
            CustomModID = testCustomModIDExists[0][0]

        # Confirms added to order
        with dpg.window(label="Add Custom Mod Confirm", width=400, height=100, tag="Add Custom Mod Confirm"):
            dpg.add_text("Custom Mod = " + str(CustomModID))

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Add Custom Mod Confirm"))

        # Add "Custom Mod" ID to modsList
        modID = SelectCustomModID()
        tempModsList.append(modID)

        # Add Custom Mod Desc to list
        customModsList.append(CustomModID)

    except Exception as e:
        logging.debug("Error: %r", e)


def AddItemToOrder(sender, app_data, user_data):
    try:
        itemID = user_data
        # Create dict to add to list of dicts (orderedItemMods)
        tempOrderedItemMods = {}
        tempOrderedItemMods.update({itemID: []})
        modList = tempOrderedItemMods[itemID]
        for mod in tempModsList:
            modList.append(mod)
        # orderedItemMods format = ({itemID: [modID, modID, etc])
        orderedItemMods.append(tempOrderedItemMods)

        # Sum cost total and create dict to add to list of dicts (orderedItemPrice)
        totalPrice = sum(tempCostList)
        tempOrderedItemPrice = {}
        tempOrderedItemPrice.update({itemID: totalPrice})
        orderedItemPrice.append(tempOrderedItemPrice)

        # Clears temp mod and cost lists for new items
        tempCostList.clear()
        tempModsList.clear()

        # Confirms added to order
        with dpg.window(label="Add Item Confirm", width=400, height=100, tag="Add Item Confirm"):
            dpg.add_text("Item added to cart!")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Add Item Confirm"))

    except Exception as e:
        logging.debug("Error: %r", e)


def CompleteOrder(sender, app_data, user_data): # UPDATES DB!!
    try:
        # Combines values in ordered Item Price to assign total order price to variable
        order_price_input_list = []
        for itemID in orderedItemPrice:
            order_price_input_list.append(sum(itemID.values()))
        order_price_input = sum(order_price_input_list)

        # Retrieve and Assign Date and Time Values (converts from list of tup to str)
        date_input = SelectDate()
        time_input = SelectTime()

        # Insert into Order Table
        newOrderID = InsertOrderSQL(str(date_input), str(time_input), order_price_input)

        # # Insert into Items per Order Table
        index = 0
        for itemIDAndPrice in orderedItemPrice:
            itemID = list(itemIDAndPrice.keys())[0]
            itemPriceInput = list(itemIDAndPrice.values())[0]

            itemNameInput = SelectNameSpecifiedItem(itemID)
            newOrderedItemID = InsertItemsPerOrderSQL(newOrderID, itemID, itemPriceInput, itemNameInput)

            # prints error message if failed
            if isinstance(newOrderedItemID, int):
                # Insert into Mods Per Ordered Item Table
                itemCustomModID = SelectCustomModID()
                itemID, modList = list(orderedItemMods[index].items())[0]
                for item in modList:
                    modID = item
                    # Adds Custom Mod if present
                    if modID == itemCustomModID:
                        name = 'Custom ID'
                        customID = customModsList.pop(0)
                        result = InsertModsPerOrderedItemCustomSQL(newOrderedItemID, modID, name, customID)
                    else:
                        name = SelectNameCostSpecifiedMod(modID)
                        result = InsertModsPerOrderedItemSQL(newOrderedItemID, modID, name)

                    # prints error message if failed
                    if isinstance(result, int):
                        pass
                    else:
                        newOrderID = result
                index += 1
            else:
                newOrderID = newOrderedItemID

        # Clear Order lists
        orderedItemMods.clear()
        orderedItemPrice.clear()

        # Opens confirmation window and prints either newOrderID or error message if failed
        with dpg.window(label="Insert Order", width=600, height=300, tag="Insert Order"):
            dpg.add_text("Order successfully added and new ID = " + str(newOrderID))

            dpg.add_button(label="Go Back Mod Menu", callback=lambda: dpg.delete_item("Insert Order"))

    except Exception as e:
        logging.debug("Error: %r", e)