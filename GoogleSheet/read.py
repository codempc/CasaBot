# This is where we read data from googlesheet and then use that data for webhook.
import gspread
import pprint
import json
import random
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate
from show_rate_responses import (
    SHOW_RATE_RESPONSE
)
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'bank_secret.json', scope)
client = gspread.authorize(creds)


def get_rate(bank_name, amount, time):
    # TODO: Get data from GoogleSheets.
    # Get from googlesheets based on the condition (bank_name, amount, time)
    rate = random.random() + 3

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
    output_string = random.choice(SHOW_RATE_RESPONSE)
    response = output_string.format(
        bank_name=bank_name,
        amount=str(amount),
        time=str(time['amount']),
        time_unit=time_unit,
        rate=round(rate, 2)

    )
    return response


def get_best_rate(bank_name="", amount="", time="", mortage_types=""):
    # TODO: Get the list of arrays from the read function from GoogleSheets.
    # TODO: Format data for the result should be in array like below
    #  (although in the real situation we should show more columns).
    result = [['CommBank', '3.2%'], ['Westpac', '3.33%'],
              ['St. George', '3.43%'], ['Suncorp', '3.57%'],
              ['ANZ', '3.6%']]
    # res = json.dumps(my_result, indent=4)
    result = tabulate(result, headers=['Bank', 'Rate'], tablefmt='orgtbl')
    return result


def view_all_data(file_name):
    sheet = client.open(file_name.lower()).sheet1
    # TODO: Get maximum and minimum loan amount for a bank.
    # TODO: Get 5 with the highest rate (no condition).
    # TODO: Get 5 with the highest rate for different bank
    # TODO: Get 5 with the highest rate for different amount of money.
    # TODO: Get 5 with the highest rate for different period
    # TODO: Get 5 with the highest rate for different mortgage types.
    pp = pprint.PrettyPrinter()
    result = sheet.get_all_records()
    pp.pprint(result)
    return result

# def get_lowest_rate(file_name, bank_name=None):
#     sheet = client.open(file_name.lower()).sheet1
#     interest_array = []
#     for interest_rate in sheet.range('E2:E80'):
#         interest_array.append(interest_rate.value)
#
#     lowest_rate = min(interest_array)
#     print(lowest_rate)
#     return lowest_rate


def get_lowest_bank(file_name, bank_name=None, mortgage=None, yearFixed=None):
    sheet = client.open(file_name.lower()).sheet1
    data = pd.DataFrame(sheet.get_all_records())
    if(bank_name is not None and mortgage is not None and yearFixed is not None):
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(yearFixed)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(bank_name is not None and mortgage is not None):
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(bank_name is not None and yearFixed is not None):
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(yearFixed)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(mortgage is not None and yearFixed is not None):
        group = data.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(yearFixed)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(bank_name is not None):
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(mortgage is not None):
        group = data.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    elif(yearFixed is not None):
        group = data.groupby('fixedInterval')
        bank_programs = group.get_group(yearFixed)
        sorted = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)
    else:
        sorted = data.sort_values(by=['interestRate'], ascending=True)
        top_lowest = sorted.head(5)

    print(top_lowest)
    return top_lowest


get_lowest_bank('casa_bank', bank_name='CommBank (CM)',
                mortgage='IO', yearFixed=1)
