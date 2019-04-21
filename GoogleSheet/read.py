# This is where we read data from googlesheet and then use that data for webhook.
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint


def get_rate(bank_name, amount, time):
    # TODO: Get data from GoogleSheets.
    rate = "4.8%"  # Get from googlesheets based on the condition (bank_name, amount, time)

    # # IF no loan amount and time, just give the first row while also giving the details. i.e.
    # if amount == "":
    #     amount = "40000"  # Get data from googlesheets first row for amount
    # if time == "":
    #     time = "30"  # Get data from googlesheets first row for time

    if time['unit'] == "mo":
        if time['amount'] > 48:
            time['amount'] = format(time['amount'] / 12.0, '.1f')
            time_unit = 'years'
        else:
            time_unit = 'month' if time['amount'] == 1 else "months"
    else:
        time_unit = 'year' if time['amount'] == 1 else "years"

    # TODO: Randomise words, not only using one.
    return "The rate for " + bank_name + " with a loan amount of " + "$" + str(amount) + " and period of " + \
        str(time['amount']) + " " + time_unit + " is " + rate


def view_all_data(file_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('bank_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open(file_name.lower()).sheet1

    pp = pprint.PrettyPrinter()
    result = sheet.get_all_records()
    pp.pprint(result)
    return result