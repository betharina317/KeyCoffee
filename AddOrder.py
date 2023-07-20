# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 7/17/23
# Module file to define Add Order Functions


from sql_statements import *
import dearpygui.dearpygui as dpg

# list of dicts
orderedItemMods = []
orderedItemPrice = []
# list of ints
tempModsList = []
tempCostList = []


def ChooseCatOrder():
    with dpg.window(label="Cat Menu", width=600, height=300, tag="Cat Menu"):
        dpg.add_text("Select which category describes the item to order:")

        # Create button for each menu category in DB
        MenuCatList = SelectAllMenuCatSQL()
        for i in MenuCatList:
            dpg.add_button(label=i, user_data=i, callback=ChooseItemOrder)

        dpg.add_button(label="Go Back to Main", callback=lambda: dpg.delete_item("Cat Menu"))


def ChooseItemOrder(sender, app_data, user_data):
    cat_input = user_data[0]
    itemList = SelectAllItem(cat_input)

    with dpg.window(label="Item Menu", width=600, height=300, tag="Item Menu"):
        dpg.add_text("Select which item you want to order:")

        # Create button for every item under selected category
        for i in itemList:
            dpg.add_button(label=i, user_data=i, callback=ChooseModOrder)

        dpg.add_button(label="Go Back to Categories", callback=lambda: dpg.delete_item("Item Menu"))


def ChooseModOrder(sender, app_data, user_data):
    item_input = user_data[0]
    tempCostList.append(user_data[2])
    modTypeList = SelectAllSpecifiedModType(item_input)

    with dpg.window(label="Mod Menu", width=600, height=300, tag="Mod Menu"):
        dpg.add_text("Select modifications for item:")

        # Create listbox for every mod type containing mods under selected item
        for i in modTypeList:
            tempModList = SelectAllSpecifiedMod(i[0])
            modList = []
            for j in tempModList:
                modList.append(j[1])
            dpg.add_listbox(label=i[1], items=modList, user_data=i[0], callback=AddMod)

        dpg.add_text("or add special instructions:")
        dpg.add_input_text(label="Special Mod", user_data=None, tag="Special Mod")
        dpg.add_button(label="Add Special Mod", user_data=dpg.get_value("Special Mod"), callback=AddSpecialMod)

        dpg.add_button(label="Add Item to Order", user_data=item_input, callback=AddItemToOrder)
        dpg.add_button(label="Order Complete", user_data=None, callback=CompleteOrder)
        dpg.add_button(label="Go Back to Items", callback=lambda: dpg.delete_item("Mod Menu"))


def AddSpecialMod(sender, app_data, user_data):
    text = dpg.get_value("Special Mod")
    print(text)

    # How to Add Special Mod to Order Tables???????


def AddMod(sender, app_data, user_data):
    name = dpg.get_value(sender)

    # Adds mod to orderedItem Dict
    tempModIDList = SelectModIDSpecifiedModType(name, user_data)
    # Converts list value to int
    modIDList = tempModIDList[0]
    modID = modIDList[0]
    tempModsList.append(modID)

    # Adds AddedCost to tempCostList
    temModCostList = SelectModCostSpecifiedModType(name, user_data)
    # Converts list to float
    modCostList = temModCostList[0]
    modCost = modCostList[0]
    tempCostList.append(modCost)


def AddItemToOrder(sender, app_data, user_data):
    # add to orderedItemMods dict
    tempOrderedItemMods = {}
    tempOrderedItemMods.update({user_data: []})
    modList = tempOrderedItemMods[user_data]
    for i in tempModsList:
        modList.append(i)
    orderedItemMods.append(tempOrderedItemMods)

    # add to orderedItemPrice dice
    totalPrice = sum(tempCostList)
    tempOrderedItemPrice = {}
    tempOrderedItemPrice.update({user_data: totalPrice})
    orderedItemPrice.append(tempOrderedItemPrice)

    # Clears temp mod and cost lists for new items
    tempCostList.clear()
    tempModsList.clear()

    # Confirms added to order
    with dpg.window(label="Add Item Confirm", width=400, height=100, tag="Add Item Confirm"):
        dpg.add_text("Item added to cart!")

        dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Add Item Confirm"))


def CompleteOrder(sender, app_data, user_data): # UPDATES DB!!
    order_price_input_list = []
    for i in orderedItemPrice:
        order_price_input_list.append(sum(i.values()))
    order_price_input = sum(order_price_input_list)

    # Retrieve and Assign Date and Time Values (converts from list of tup to str)
    tempDateList = SelectDate()
    tempDateTup = tempDateList[0]
    date_input = tempDateTup[0]
    tempTimeList = SelectTime()
    tempTimeTup = tempTimeList[0]
    time_input = tempTimeTup[0]

    # Insert into Order Table
    newOrderID = InsertOrderSQL(str(date_input), str(time_input), order_price_input)

    # # Insert into Items per Order Table
    for i in orderedItemPrice:
        itemID, item_price_input = list(i.items())[0]

        item_name_input = SelectNameSpecifiedItem(itemID)

        newOrderedItemID = InsertItemsPerOrderSQL(newOrderID, itemID, item_price_input, item_name_input)

        # prints error message if failed
        if isinstance(newOrderedItemID, int):
            pass
        else:
            newOrderID = newOrderedItemID

        # Insert into Mods Per Ordered Item Table
        for j in orderedItemMods:
            itemID, modList = list(j.items())[0]
            for k in modList:
                modID = k

                # converts list of tup to str
                tempNameList = SelectNameCostSpecifiedMod(modID)
                tempNameTup = tempNameList[0]
                name = tempNameTup[0]

                result = InsertModsPerOrderedItemSQL(newOrderedItemID, modID, name)

                # prints error message if failed
                if isinstance(result, int):
                    pass
                else:
                    newOrderID = result

    with dpg.window(label="Insert Order", width=600, height=300, tag="Insert Order"):
        dpg.add_text("Order successfully added and new ID = " + str(newOrderID))

        dpg.add_button(label="Go Back Mod Menu", user_data=None, callback=lambda: dpg.delete_item("Insert Order"))
