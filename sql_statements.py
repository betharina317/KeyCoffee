# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 7/27/23
# Module file to define SQL Functions

import sqlite3
import logging

logging.basicConfig(filename='KeyCoffee.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


# Re-Usable Code Example!!!
def QueryDB(query, *args):
    try:
        connection = sqlite3.connect(r'C:\Users\andrew\Desktop\KeyCoffeeDB/KeyCoffee.db')
        cursor = connection.cursor()

        # Selects given columns from given table
        cursor.execute(query, args)
        result = (cursor.fetchall())

        connection.commit() # !! Changes DB
        cursor.close()
        return result

    except sqlite3.Error as error:
        errorMess = ("Error while connecting to sqlite: ", error)
        logging.debug(errorMess)
        return errorMess

    finally:
        if connection:
            connection.close()


# Re-Usable Code Example!!!
def InsertQueryDB(query, *args):
    try:
        connection = sqlite3.connect(r'C:\Users\andrew\Desktop\KeyCoffeeDB/KeyCoffee.db')
        cursor = connection.cursor()

        # Selects given columns from given table
        cursor.execute(query, args)
        result = cursor.lastrowid

        connection.commit() # !! Changes DB
        cursor.close()
        return result

    except sqlite3.Error as error:
        errorMess = ("Error while connecting to sqlite: ", error)
        logging.debug(errorMess)
        return errorMess

    finally:
        if connection:
            connection.close()


# ############# SELECT STATEMENTS ######################


def SelectDate():
    query = "select date('now','localtime')"
    date = QueryDB(query)
    return date[0][0]


def SelectTime():
    query = "select time('now','localtime')"
    time = QueryDB(query)
    return time[0][0]


def SelectAllMenuCatSQL():
    query = "select * from Menu_Cat_LU"
    listOfTuples = QueryDB(query)
    return listOfTuples


def SelectAllSpecifiedModType(itemID):
    # Displays Mod Type Options
    query = "select ID, Name from Item_Mod_Type where ItemID = (?)"
    result = QueryDB(query, itemID)
    return result


def SelectNameSpecifiedModType(type_input):
    # Displays Mod Type Options
    query = "select Name from Item_Mod_Type where ID = (?)"
    result = QueryDB(query, type_input)
    return result


def SelectAllSpecifiedMod(type_input):
    # Displays Mod Options under type
    query = "select ID, Name from Item_Mod where ItemModTypeID = (?)"
    result = QueryDB(query, type_input)
    return result


def SelectNameCostSpecifiedMod(mod_input):
    # Displays specific Mod info
    query = "select Name, AddedCost from Item_Mod where ID = (?)"
    result = QueryDB(query, mod_input)
    return result[0][0]


def SelectIDNameItem(cat_input):
    # Displays Mod Type Options
    query = "select ID, Name from Item where MenuCatID = (?)"
    result = QueryDB(query, cat_input)
    return result


def SelectAllItem(cat_input):
    # Displays Mod Type Options
    query = "select ID, Name, Price from Item where MenuCatID = (?)"
    result = QueryDB(query, cat_input)
    return result


def SelectNamePriceSpecifiedItem(item_input):
    query = "select Name, Price from Item where ID = (?)"
    result = QueryDB(query, item_input)
    return result


def SelectNameSpecifiedItem(item_input): # KEEP
    query = "select Name from Item where ID = (?)"
    result = QueryDB(query, item_input)
    return result[0][0]


def SelectModIDSpecifiedModType(name, type_input): # KEEP
    query = "select ID from Item_Mod where Name = (?) and ItemModTypeID = (?)"
    result = QueryDB(query, name, type_input)
    return result[0][0]


def SelectModCostSpecifiedModType(name, type_input): # KEEP
    query = "select AddedCost from Item_Mod where Name = (?) and ItemModTypeID = (?)"
    result = QueryDB(query, name, type_input)
    return result[0][0]


def SelectExistingCustomMod(description):
    query = "select ID from Custom_Mod where Description like (?)"
    result = QueryDB(query, description)
    return result


def SelectCustomModID():
    query = "Select ID from Item_MOD where (Name) = ('Custom Mod')"
    result = QueryDB(query)
    return result[0][0]


def SelectOrdersForDateRange(startDate, endDate):
    query = "Select * from Orders where Date between (?) and (?)"
    result = QueryDB(query, startDate, endDate)
    return result


def SelectOrdersItemsMods(startDate, endDate):
    query = "select OrderID, Date, Time, ItemID, MenuItemName, ItemPrice, group_concat(ItemModName) from " \
            "(select o.ID as OrderID, Date, Time, i.ID as ItemID, MenuItemName, i.TotalPrice as ItemPrice, " \
            "ItemModName from Orders as o " \
            "inner join Items_Per_Order as i on o.ID = i.OrderID " \
            "inner join Mods_Per_Ordered_Item as m on i.ID = m.OrderedITemID " \
            "where Date between (?) and (?))" \
            "group by OrderID, ItemID"

    result = QueryDB(query, startDate, endDate)
    return result


def SelectCustomMods(startDate, endDate):
    query = "select o.ID as OrderID, Date, Time, i.ID as ItemID, MenuItemName, CustomModID, " \
            "c.Description as CustomModName from Orders as o " \
            "inner join Items_Per_Order as i on o.ID = i.OrderID " \
            "inner join Mods_Per_Ordered_Item as m on i.ID = m.OrderedITemID " \
            "inner join Custom_Mod as c on m.CustomModID = c.ID " \
            "where Date between (?) and (?)" \
            "group by OrderID, ItemID"

    result = QueryDB(query, startDate, endDate)
    return result


def SelectMostFrequentCustomMod(startDate, endDate):
    query = "select Description, count(*) as Count from Mods_Per_Ordered_Item as m " \
            "inner join Custom_Mod as c on m.CustomModID = c.ID " \
            "inner join Items_Per_Order as i on m.OrderedItemID = i.ID " \
            "inner join Orders as o on i.OrderID = o.ID " \
            "where Date between (?) and (?) " \
            "group by Description order by count(*) desc"

    result = QueryDB(query, startDate, endDate)
    return result

# ############# VERIFY STATEMENTS ######################


def ValidItemChoices():
    # Add available Item IDs to variable for verification purposes
    query = "select ID from Item"
    listOfTuples = QueryDB(query)
    # converts list of tuples to list of ints for validation purposes
    result = [i[0] for i in listOfTuples]
    return result


def ValidModTypeChoices(itemID):
    # Add available Mod Type IDs to variable for verification purposes
    query = "select ID from Item_Mod_Type where ItemID = (?)"
    listOfTuples = QueryDB(query, itemID)
    # converts list of tuples to list of ints for validation purposes
    result = [i[0] for i in listOfTuples]
    return result


def ValidModChoices(type_input):
    # Add available Mod Type IDs to variable for verification purposes
    query = "select ID from Item_Mod where ItemModTypeID = (?)"
    listOfTuples = QueryDB(query, type_input)
    # converts list of tuples to list of ints for validation purposes
    result = [i[0] for i in listOfTuples]
    return result


# #############  DELETE STATEMENTS ######################


def DeleteItemSQL(item_input):
    # Deletes Item from Item Table (changes should cascade through Mod Type/Mod Tables)
    query = "delete from Item where ID = (?)"
    result = QueryDB(query, item_input)
    return result


def DeleteModTypeSQL(type_input):
    # Deletes Item from Item_Mod_Type Table (changes should cascade through Mod Table)
    query = "delete from Item_Mod_Type where ID = (?)"
    result = QueryDB(query, type_input)
    return result


def DeleteModSQL(mod_input):
    # Deletes mod from Item_Mod Table
    query = "delete from Item_Mod where ID = (?)"
    result = QueryDB(query, mod_input)
    return result


# ############# INSERT STATEMENTS ######################


def InsertItemSQL(cat_input, name_input, price_input):
    # Insert into Item Table
    query = "INSERT INTO Item (MenuCatID, Name, Price) VALUES (?,?,?)"
    result = InsertQueryDB(query, cat_input, name_input, price_input)
    return result


def InsertItemModTypeSQL(modTypeName_input, itemID):
    # Insert values into Item Mod Type Table
    query = "INSERT INTO Item_Mod_Type (Name, ItemID) VALUES (?,?)"
    result = InsertQueryDB(query, modTypeName_input, itemID)
    return result


def InsertItemModSQL(modTypeID_input, modName_input, addedCost_input):
    # Insert values into Item_Mod Table
    query = "INSERT INTO Item_Mod (ItemModTypeID, Name, AddedCost) VALUES (?,?,?)"
    result = InsertQueryDB(query, modTypeID_input, modName_input, addedCost_input)
    return result


def InsertOrderSQL(date_input, time_input, price_input):
    # Insert into Orders Table
    query = "INSERT INTO Orders (Date, Time, TotalPrice) VALUES (?,?,?)"
    result = InsertQueryDB(query, date_input, time_input, price_input)
    return result


def InsertItemsPerOrderSQL(orderID_input, menuItemID_input, totalPrice_input, name_input):
    # Insert into ItemsPerOrder Table
    query = "INSERT INTO Items_Per_Order (OrderID, MenuItemID, TotalPrice, MenuItemName) VALUES (?,?,?, ?)"
    result = InsertQueryDB(query, orderID_input, menuItemID_input, totalPrice_input, name_input)
    return result


def InsertModsPerOrderedItemSQL(OrderedItemID_input, itemModID_input, name_input):
    # Insert into ModsPerOrderedItem Table
    query = "INSERT INTO Mods_Per_Ordered_Item (OrderedItemID, ItemModID, ItemModName) VALUES (?,?,?)"
    result = InsertQueryDB(query, OrderedItemID_input, itemModID_input, name_input)
    return result


def InsertModsPerOrderedItemCustomSQL(OrderedItemID_input, itemModID_input, name_input, custom_input):
    # Insert into ModsPerOrderedItem Table
    query = "INSERT INTO Mods_Per_Ordered_Item (OrderedItemID, ItemModID, ItemModName, CustomModID) VALUES (?,?,?,?)"
    result = InsertQueryDB(query, OrderedItemID_input, itemModID_input, name_input, custom_input)
    return result


def InsertCustomModSQL(description_input): # AUTO FILLS IN CUSTOM MOD ID '97'
    customModID = SelectCustomModID()
    query = "INSERT INTO Custom_Mod (ItemModCustomID, Description) VALUES (?, ?)"
    result = InsertQueryDB(query, customModID, description_input)
    return result

# ############# UPDATE STATEMENTS ######################


def UpdateItemName(new_name, item_input):
    query = "update Item set Name = (?) where ID = (?)"
    result = QueryDB(query, new_name, item_input)
    return result


def UpdateItemPrice(new_price, item_input):
    query = "update Item set Price = (?) where ID = (?)"
    result = QueryDB(query, new_price, item_input)
    return result


def UpdateItemModType(new_name, type_input):
    query = "update Item_Mod_Type set Name = (?) where ID = (?)"
    result = QueryDB(query, new_name, type_input)
    return result


def UpdateModName(new_name, mod_input):
    query = "update Item_Mod set Name = (?) where ID = (?)"
    result = QueryDB(query, new_name, mod_input)
    return result


def UpdateModAddedCost(new_price, mod_input):
    query = "update Item_Mod set AddedCost = (?) where ID = (?)"
    result = QueryDB(query, new_price, mod_input)
    return result
