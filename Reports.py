# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 7/31/23
# Module file to define Add Order Functions

from sql_statements import *
import dearpygui.dearpygui as dpg
import xlsxwriter


def ReportsMenu(sender, app_data, user_data):
    try:
        with dpg.window(label="Reports Menu", width=400, height=150, tag="Reports Menu"):
            dpg.delete_item("Verify Login Window")

            # Reports Menu Options
            dpg.add_button(label="Revenue Report", user_data=GenerateRevReport, callback=EnterDateRange,
                           tag="Revenue Report")
            dpg.add_button(label="Order Details Report", user_data=GenerateDetailReport, callback=EnterDateRange,
                           tag="Order Details Report")
            dpg.add_button(label="Custom Mods Report", user_data=GenerateCustomModsReport, callback=EnterDateRange,
                           tag="Custom Mods Report")

            dpg.add_button(label="Back to Admin Menu", user_data=None, callback=lambda: dpg.delete_item("Reports Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


# Re-Used Code!!
def EnterDateRange(sender, app_data, user_data):
    try:
        with dpg.window(label="Enter Report Date Range", width=400, height=300, tag="Enter Report Date Range"):

            # Receives date range for reports
            dpg.add_text("Enter Start Date (YYYY-MM-DD):")
            dpg.add_input_text(tag="Start Date", scientific=True)
            dpg.add_text("Enter End Date (YYYY-MM-DD):")
            dpg.add_input_text(tag="End Date", scientific=True)
            dpg.add_button(label="Generate Report", callback=user_data, tag="Generate Report")
            print(user_data)
            print(type(user_data))

            dpg.add_button(label="Back to Reports Menu", user_data=None,
                           callback=lambda: dpg.delete_item("Enter Report Date Range"))

    except Exception as e:
        logging.debug("Error: %r", e)


def GenerateRevReport(sender, app_data, user_data):

    try:
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(downloads_path + '\Orders.xlsx')
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some data headers.
        worksheet.write('A1', 'OrderID', bold)
        worksheet.write('B1', 'Date', bold)
        worksheet.write('C1', 'Time', bold)
        worksheet.write('D1', 'TotalPrice', bold)

        # Obtain data and set starting row/col
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        revData = SelectOrdersForDateRange(startDate, endDate)
        row = 1
        col = 0

        # write data to spreadsheet
        for id, date, time, price in revData:
            worksheet.write(row, col, id)
            worksheet.write(row, col + 1, date)
            worksheet.write(row, col + 2, time)
            worksheet.write(row, col + 3, price)
            row += 1
        # Make last row total values
        worksheet.write(row, col, 'Total Revenue', bold)
        worksheet.write(row, col + 3, '=SUM(D1:D{})'.format(row))

        # Make cells autofit data and close workbook
        worksheet.autofit()
        workbook.close()

        with dpg.window(label="Report Generated", width=400, height=100, tag="Report Generated"):
            # Confirm success
            dpg.add_text("Revenue Report Downloaded")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Report Generated", width=400, height=100, tag="Report Generated"):
            # Print failure
            dpg.add_text("Error Downloading Rev Report")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Report Generated"))


def GenerateDetailReport(sender, app_data, user_data):

    try:
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(downloads_path + '\OrderDetails.xlsx')
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some data headers.
        worksheet.write('A1', 'OrderID', bold)
        worksheet.write('B1', 'Date', bold)
        worksheet.write('C1', 'Time', bold)
        worksheet.write('D1', 'ItemID', bold)
        worksheet.write('E1', 'MenuItemName', bold)
        worksheet.write('F1', 'ItemPrice', bold)
        worksheet.write('G1', 'ItemModName(s)', bold)

        # Obtain data and set starting row/col
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        detData = SelectOrdersItemsMods(startDate, endDate)
        row = 1
        col = 0

        # Write data to spreadsheet
        for OrderID, Date, Time, ItemID, MenuItemName, ItemPrice, ItemModName in detData:
            worksheet.write(row, col, OrderID)
            worksheet.write(row, col + 1, Date)
            worksheet.write(row, col + 2, Time)
            worksheet.write(row, col + 3, ItemID)
            worksheet.write(row, col + 4, MenuItemName)
            worksheet.write(row, col + 5, ItemPrice)
            worksheet.write(row, col + 6, ItemModName)
            row += 1

        # Make worksheet cells autofit and close workbook
        worksheet.autofit()
        workbook.close()

        with dpg.window(label="Detail Report Generated", width=400, height=100, tag="Detail Report Generated"):
            # Print Success
            dpg.add_text("Order Details Report Downloaded")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Detail Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Detail Report Error", width=400, height=100, tag="Detail Report Error"):
            # Print Failure
            dpg.add_text("Error Downloading Details Report: " + str(myData))

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Detail Report Error"))


def GenerateCustomModsReport(sender, app_data, user_data):

    try:
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(downloads_path + '\CustomMods.xlsx')
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Write some data headers.
        worksheet.write('A1', 'OrderID', bold)
        worksheet.write('B1', 'Date', bold)
        worksheet.write('C1', 'Time', bold)
        worksheet.write('D1', 'ItemID', bold)
        worksheet.write('E1', 'MenuItemName', bold)
        worksheet.write('F1', 'CustomModID', bold)
        worksheet.write('G1', 'CustomModName', bold)
        worksheet.write('H1', 'Most Ordered Mods', bold)
        worksheet.write('I1', 'Count', bold)

        # Obtain data and set starting row/col
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        custData = SelectCustomMods(startDate, endDate)
        mostMod = SelectMostFrequentCustomMod(startDate, endDate)
        row = 1
        col = 0

        # Write data to spreadsheet
        for OrderID, Date, Time, ItemID, MenuItemName, CustomModID, CustomModName in custData:
            worksheet.write(row, col, OrderID)
            worksheet.write(row, col + 1, Date)
            worksheet.write(row, col + 2, Time)
            worksheet.write(row, col + 3, ItemID)
            worksheet.write(row, col + 4, MenuItemName)
            worksheet.write(row, col + 5, CustomModID)
            worksheet.write(row, col + 6, CustomModName)
            row += 1
        # Add analysis of most order custom mod
        row = 1
        for Description, Count in mostMod:
            worksheet.write(row, col + 7, Description)
            worksheet.write(row, col + 8, Count)
            row += 1

        # Make worksheet cells autofit and close workbook
        worksheet.autofit()
        workbook.close()

        with dpg.window(label="Custom Mods Report Generated", width=400, height=100, tag="Custom Mods Report Generated"):
            # Print Success
            dpg.add_text("Custom Mods Report Downloaded")

            dpg.add_button(label="Close", user_data=None,
                           callback=lambda: dpg.delete_item("Custom Mods Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Custom Mods Report Error", width=400, height=100, tag="Custom Mods Report Error"):
            # Print Failure
            dpg.add_text("Error Downloading Custom Mods Report")

            dpg.add_button(label="Close", user_data=None,
                           callback=lambda: dpg.delete_item("Custom Mods Report Error"))