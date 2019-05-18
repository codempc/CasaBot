# This is where we read data from googlesheet and then use that data for webhook.
import gspread
import pprint
import json
import random
import os
import time
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(dir_path + '/bank_secret.json', scope)
client = gspread.authorize(creds)


def get_best_rate(bank_name=None, mortgage_types=None, year_fixed=None, ownership_status=None):
    # TODO: Get the list of arrays from the get_lowest_bank function from GoogleSheets.
    # TODO: Format data for the result should be in array like below
    #  (although in the real situation we should show more columns).

    result = get_lowest_bank(bank_name, mortgage_types, year_fixed, ownership_status)

    bank = result['Bank_name'].item()
    repayment_type = result['Repayment_type'].item()
    year_fixed = result['Fixed_year'].item()
    interest = result['Interest_rate'].item()
    ownership = result['Ownership_status'].item()
    details = {
        "bank_name": bank,
        "repayment_type": repayment_type,
        "year_fixed": year_fixed,
        "ownership": ownership_status,
        "interest_rate": interest
    }

    return details

    # content = "The rate from " + bank + " with " + mortgage + " mortgage type and " \
    #           + str(year) + " year(s) fixed rate is " + str(interest) + "%."
    # return content


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

def get_lowest_rate_group_by(data, params):
    group = None
    bank_programs = None
    for key, value in params.items():
        if value is not None:
            if group is None:
                group = data.groupby(key)
                bank_programs = group.get_group(value)
            else:
                group = bank_programs.groupby(key)
                bank_programs = group.get_group(value)

    if bank_programs is not None:
        result = bank_programs.sort_values(by=['Interest_rate'], ascending=True)
    else:
        result = data.sort_values(by=['Interest_rate'], ascending=True)
    return result.head(1)


def get_lowest_bank(bank_name=None, mortgage=None, year_fixed=None, ownership_status=None):
    # start = time.time()
    sheet = client.open('casa_bank').sheet1
    # end = time.time()
    # print("lowest", end - start)

    data = pd.DataFrame(sheet.get_all_records())
    params = {
        "Bank_name": bank_name,
        "Repayment_type": mortgage,
        "Fixed_year": year_fixed,
        "Ownership_status": ownership_status
    }

    return get_lowest_rate_group_by(data, params)

# Example:
# get_lowest_bank(bank_name='CommBank (CM)',
#                 mortgage='IO', yearFixed=1)

# get_lowest_bank('CommBank (CM)')
# start = time.time()
# print(get_best_rate())
# end = time.time()
# print(end - start)
#print(get_best_rate('CommBank'))
