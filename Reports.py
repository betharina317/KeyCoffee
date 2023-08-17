# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 8/16/23
# Module file to define Add Order Functions

from sql_statements import *
import dearpygui.dearpygui as dpg
import xlsxwriter


# Re-Used Code!!
def EnterDateRange(sender, app_data, user_data):
    try:
        with dpg.window(label="Enter Report Date Range", width=400, height=300, tag="Enter Report Date Range"):
            dpg.delete_item("Verify Pin Window")

            # Receives date range for reports
            dpg.add_text("Enter Start Date (YYYY-MM-DD):")
            dpg.add_input_text(tag="Start Date", scientific=True)
            dpg.add_text("Enter End Date (YYYY-MM-DD):")
            dpg.add_input_text(tag="End Date", scientific=True)

            # Reports Menu Options
            dpg.add_button(label="Revenue Report", callback=GenerateRevReport, tag="Revenue Report")
            dpg.add_button(label="Order Details Report", callback=GenerateDetailReport, tag="Order Details Report")
            dpg.add_button(label="Custom Mods Report", callback=GenerateCustomModsReport, tag="Custom Mods Report")

            dpg.add_button(label="Back to Admin Menu", callback=lambda: dpg.delete_item("Reports Menu"))

    except Exception as e:
        logging.debug("Error: %r", e)


# Re-Used Code
def WriteWorksheet(filename, headerList, data):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(downloads_path + filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Write some data headers.
    for tup in headerList:
        col = tup[0]
        header = tup[1]
        worksheet.write(col, header, bold)

    # Convert data to worksheet
    row = 1
    for tuple in enumerate(data):
        col = 0
        for value in tuple[1]:
            worksheet.write(row, col, value)
            col += 1
        row += 1

    # Additional data for specified files
    if filename == '/Orders.xlsx':
        # Make last row total values
        col = 0
        worksheet.write(row, col, 'Total Revenue', bold)
        worksheet.write(row, col + 3, '=SUM(D1:D{})'.format(row))

    elif filename == '\CustomMods.xlsx':
        # Add analysis of most order custom mod
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        mostMod = SelectMostFrequentCustomMod(startDate, endDate)
        col = 0
        row = 1
        for Description, Count in mostMod:
            worksheet.write(row, col + 7, Description)
            worksheet.write(row, col + 8, Count)
            row += 1
    else:
        pass

    # Make cells autofit data and close workbook
    worksheet.autofit()
    workbook.close()


def GenerateRevReport(sender, app_data, user_data):

    try:
        revFilename = '/Orders.xlsx'
        revHeaderList = [('A1', 'OrderID'), ('B1', 'Date'), ('C1', 'Time'), ('D1', 'TotalPrice')]
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        revData = SelectOrdersForDateRange(startDate, endDate)

        WriteWorksheet(revFilename, revHeaderList, revData)

        with dpg.window(label="Report Generated", width=400, height=100, tag="Report Generated"):
            # Confirm success
            dpg.add_text("Revenue Report Downloaded")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Revenue Report Error", width=400, height=100, tag="Revenue Report Error"):
            # Print failure
            dpg.add_text("Error Downloading Rev Report")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Revenue Report Error"))


def GenerateDetailReport(sender, app_data, user_data):

    try:
        detFilename = '\OrderDetails.xlsx'
        detHeaderList = [('A1', 'OrderID'), ('B1', 'Date'), ('C1', 'Time'), ('D1', 'ItemID'), ('E1', 'MenuItemName'),
                         ('F1', 'ItemPrice'), ('G1', 'ItemMod(s)')]
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        detData = SelectOrdersItemsMods(startDate, endDate)

        WriteWorksheet(detFilename, detHeaderList, detData)

        with dpg.window(label="Detail Report Generated", width=400, height=100, tag="Detail Report Generated"):
            # Print Success
            dpg.add_text("Order Details Report Downloaded")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Detail Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Detail Report Error", width=400, height=100, tag="Detail Report Error"):
            # Print Failure
            dpg.add_text("Error Downloading Details Report: ")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Detail Report Error"))


def GenerateCustomModsReport(sender, app_data, user_data):

    try:
        custFilename = '\CustomMods.xlsx'
        custHeaderList = [('A1', 'OrderID'), ('B1', 'Date'), ('C1', 'Time'), ('D1', 'ItemID'), ('E1', 'MenuItemName'),
                         ('F1', 'CustomModID'), ('G1', 'CustomModName'), ('H1', 'Most Ordered Mods'), ('I1', 'Count')]
        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        custData = SelectCustomMods(startDate, endDate)

        WriteWorksheet(custFilename, custHeaderList, custData)

        with dpg.window(label="Custom Mods Report Generated", width=400, height=100, tag="Custom Mods Report Generated"):
            # Print Success
            dpg.add_text("Custom Mods Report Downloaded")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Custom Mods Report Generated"))

    except Exception as e:
        logging.debug("Error: %r", e)

        with dpg.window(label="Custom Mods Report Error", width=400, height=100, tag="Custom Mods Report Error"):
            # Print Failure
            dpg.add_text("Error Downloading Custom Mods Report")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("Custom Mods Report Error"))