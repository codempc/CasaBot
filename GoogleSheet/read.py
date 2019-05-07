# This is where we read data from googlesheet and then use that data for webhook.
import gspread
import pprint
import json
import random
import os
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate
import pandas as pd
from show_rate_responses import (
    SHOW_RATE_RESPONSE
)

dir_path = os.path.dirname(os.path.realpath(__file__))
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(dir_path + '/bank_secret.json', scope)
client = gspread.authorize(creds)


def get_show_rate(bank_name, repayment_type):
    # TODO: Get data from GoogleSheets.
    # Get from googlesheets based on the condition (bank_name, amount, time)
    rate = random.random() + 3

    # # IF no loan amount and time, just give the first row while also giving the details. i.e.
    # if amount == "":
    #     amount = "40000"  # Get data from googlesheets first row for amount
    # if time == "":
    #     time = "30"  # Get data from googlesheets first row for time
    # TODO: Get maximum and minimum loan amount for a bank.

    # TODO: Fixed the required parameters for show rate.
    # if time['unit'] == "mo":
    #     if time['amount'] > 48:
    #         time['amount'] = format(time['amount'] / 12.0, '.1f')
    #         time_unit = 'years'
    #     else:
    #         time_unit = 'month' if time['amount'] == 1 else "months"
    # else:
    #     time_unit = 'year' if time['amount'] == 1 else "years"

    result = get_lowest_bank(bank_name, repayment_type)

    repayment_type = result['repaymentType'].item()
    rate = result['interestRate'].item()

    output_string = random.choice(SHOW_RATE_RESPONSE)
    response = output_string.format(
        bank_name=bank_name,
        repayment_type=repayment_type,
        rate=round(rate, 2)
    )
    return response


def get_best_rate(bank_name=None, mortgage_types=None, year_fixed=None):
    # TODO: Get the list of arrays from the get_lowest_bank function from GoogleSheets.
    # TODO: Format data for the result should be in array like below
    #  (although in the real situation we should show more columns).

    result = get_lowest_bank(bank_name, mortgage_types, year_fixed)

    bank = result['Bank_Name'].item()
    mortgage = result['repaymentType'].item()
    year = result['fixedInterval'].item()
    interest = result['interestRate'].item()

    content = "The rate from " + bank + " with " + mortgage + " mortgage type and " \
              + str(year) + " year(s) fixed rate is " + str(interest) + "%."
    # # How many is received from the result.
    # row_length = len(result['Bank_Name'])
    # # How many column.
    # column_length = len(result)
    # headers = []
    # content = [[0]*column_length for i in range(row_length)]
    #
    # # Iterate through the dictionary.
    # for index, value in enumerate(result.items()):
    #     headers.append(value[0])
    #     # print(key, value)
    #     for childIndex, childValue in enumerate(value[1].items()):
    #         content[childIndex][index] = (childValue[1])
    #

    # res = json.dumps(my_result, indent=4)
    # content = tabulate(content, headers=headers, tablefmt='orgtbl')
    return content


def view_all_data(file_name):
    sheet = client.open(file_name.lower()).sheet1
    # TODO: Get 5 with the highest rate (no condition).
    # TODO: Get 5 with the highest rate for different bank
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


def get_lowest_bank(bank_name=None, mortgage=None, year_fixed=None):
    sheet = client.open('casa_bank').sheet1
    data = pd.DataFrame(sheet.get_all_records())
    if bank_name is not None and mortgage is not None and year_fixed is not None:
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(year_fixed)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif bank_name is not None and mortgage is not None:
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif bank_name is not None and year_fixed is not None:
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(year_fixed)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif mortgage is not None and year_fixed is not None:
        group = data.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        group = bank_programs.groupby('fixedInterval')
        bank_programs = group.get_group(year_fixed)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif bank_name is not None:
        group = data.groupby('Bank_Name')
        bank_programs = group.get_group(bank_name)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif mortgage is not None:
        group = data.groupby('repaymentType')
        bank_programs = group.get_group(mortgage)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    elif year_fixed is not None:
        group = data.groupby('fixedInterval')
        bank_programs = group.get_group(year_fixed)
        result = bank_programs.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)
    else:
        result = data.sort_values(by=['interestRate'], ascending=True)
        top_lowest = result.head(1)

    return top_lowest


# Example:
# get_lowest_bank(bank_name='CommBank (CM)',
#                 mortgage='IO', yearFixed=1)

#get_lowest_bank('CommBank (CM)')

print(get_best_rate('CommBank', 'IO', 1))
