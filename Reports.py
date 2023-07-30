# Elizabeth Vickerman- KeyCoffee Project
# Last Edited 7/27/23
# Module file to define Add Order Functions

from sql_statements import *
import dearpygui.dearpygui as dpg
import xlsxwriter
from pathlib import Path

# Finds user's downloads path
downloads_path = str(Path.home() / "Downloads")


def ReportsMenu(sender, app_data, user_data):

    with dpg.window(tag="Reports Menu"):
        dpg.add_button(label="Revenue Report", callback=GenTransReport, tag="Revenue Report")
        dpg.add_button(label="Order Details Report", callback=GenOrderDetailsReport, tag="Order Details Report")
        dpg.add_button(label="TBD1", callback=None, tag="TBD1")

        dpg.add_button(label="Back to Main Menu", user_data=None, callback=lambda: dpg.delete_item("Reports Menu"))


def GenTransReport(sender, app_data, user_data):

    # Confirms added to order
    with dpg.window(label="Generate Trans Report", width=400, height=300, tag="Generate Trans Report"):
        dpg.add_text("Enter Start Date (YYYY-MM-DD):")
        dpg.add_input_text(tag="Start Date", scientific=True)
        dpg.add_text("Enter End Date (YYYY-MM-DD):")
        dpg.add_input_text(tag="End Date", scientific=True)
        dpg.add_button(label="Generate Revenue Report", callback=ConfirmRevReportGenerated,
                       tag="Generate Revenue Report")

        dpg.add_button(label="Back to Reports Menu", user_data=None,
                       callback=lambda: dpg.delete_item("Generate Trans Report"))


def GenOrderDetailsReport(sender, app_data, user_data):

    # Confirms added to order
    with dpg.window(label="Generate Details Report", width=400, height=300, tag="Generate Details Report"):
        dpg.add_text("Enter Start Date (YYYY-MM-DD):")
        dpg.add_input_text(tag="Start Date", scientific=True)
        dpg.add_text("Enter End Date (YYYY-MM-DD):")
        dpg.add_input_text(tag="End Date", scientific=True)
        dpg.add_button(label="Generate Order Details Report", callback=ConfirmDetailReportGenerated,
                       tag="Generate Order Details Report")

        dpg.add_button(label="Back to Reports Menu", user_data=None,
                       callback=lambda: dpg.delete_item("Generate Details Report"))


def ConfirmRevReportGenerated(sender, app_data, user_data):

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

        startDate = dpg.get_value("Start Date")
        endDate = dpg.get_value("End Date")
        myData = SelectOrdersForDateRange(startDate, endDate)
        row = 1
        col = 0

        for id, date, time, price in myData:
            worksheet.write(row, col, id)
            worksheet.write(row, col + 1, date)
            worksheet.write(row, col + 2, time)
            worksheet.write(row, col + 3, price)
            row += 1
        worksheet.write(row, col, 'Total Revenue', bold)
        worksheet.write(row, col + 3, '=SUM(D1:D{})'.format(row))

        workbook.close()

        with dpg.window(label="Report Generated", width=400, height=100, tag="Report Generated"):
            dpg.add_text("Revenue Report Downloaded")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Report Generated"))

    except:

        with dpg.window(label="Report Generated", width=400, height=100, tag="Report Generated"):
            dpg.add_text("Error Downloading Rev Report")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Report Generated"))

# TBD: Add CustomModName and autosize cells to fit values


def ConfirmDetailReportGenerated(sender, app_data, user_data):

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
        worksheet.write('G1', 'ItemModName', bold)
        worksheet.write('H1', 'CustomModName', bold)

        # startDate = dpg.get_value("Start Date")
        # endDate = dpg.get_value("End Date")
        myData = SelectOrdersItemsMods()
        print(myData)
        row = 1
        col = 0

        for OrderID, Date, Time, ItemID, MenuItemName, ItemPrice, ItemModName, CustomModName in myData:
            worksheet.write(row, col, OrderID)
            worksheet.write(row, col + 1, Date)
            worksheet.write(row, col + 2, Time)
            worksheet.write(row, col + 3, ItemID)
            worksheet.write(row, col + 4, MenuItemName)
            worksheet.write(row, col + 5, ItemPrice)
            worksheet.write(row, col + 6, ItemModName)
            worksheet.write(row, col + 7, CustomModName)
            row += 1

        workbook.close()

        with dpg.window(label="Detail Report Generated", width=400, height=100, tag="Detail Report Generated"):
            dpg.add_text("Order Details Report Downloaded")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Detail Report Generated"))

    except:

        with dpg.window(label="Detail Report Generated", width=400, height=100, tag="Detail Report Generated"):
            dpg.add_text("Error Downloading Details Report")

            dpg.add_button(label="Close", user_data=None, callback=lambda: dpg.delete_item("Detail Report Generated"))




