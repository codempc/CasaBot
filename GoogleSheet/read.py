# This is where we read data from googlesheet and then use that data for webhook.
import gspread
import pprint
import json
import random
import os
import time
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate
from functools import lru_cache

dir_path = os.path.dirname(os.path.realpath(__file__))
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(dir_path + '/bank_secret.json', scope)
client = gspread.authorize(creds)

def view_all_data(file_name):
    sheet = client.open(file_name).sheet1
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

def open_sheet():
    
    # mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # print(type(mc.get('sheet')))
    # if mc.get('sheet') is None:
    #     sheet = client.open('Bank_Chatbot_Data').sheet1
    #     mc.set('sheet', sheet)
    # else:
    #     sheet = mc.get('sheet')

    # return sheet
    start = time.time()
    sheet = client.open('Bank_Chatbot_Data').sheet1
    end = time.time()
    print(end - start)
    return sheet

def get_best_rate(bank_name=None, mortgage=None, year_fixed=None, ownership_status=None):
    start = time.time()
    sheet = open_sheet()
    end = time.time()
    print(end - start)

    data = pd.DataFrame(sheet.get_all_records())
    params = {
        "Bank_name": bank_name,
        "Repayment_type": mortgage,
        "Fixed_year": year_fixed,
        "Ownership_status": ownership_status
    }

    best_rate = get_lowest_rate_group_by(data, params)

    bank = best_rate['Bank_name'].item()
    repayment_type = best_rate['Repayment_type'].item()
    year_fixed = best_rate['Fixed_year'].item()
    interest = best_rate['Interest_rate'].item()
    ownership = best_rate['Ownership_status'].item()
    
    details = {
        "bank_name": bank,
        "repayment_type": repayment_type,
        "year_fixed": year_fixed,
        "ownership": ownership,
        "interest_rate": interest
    }

    return details

def get_last_updated():
    sheet = open_sheet()
    
    return sheet.acell('K2').value



# Example:
# get_lowest_bank(bank_name='CommBank (CM)',
#                 mortgage='IO', yearFixed=1)

# get_lowest_bank('CommBank (CM)')
# start = time.time()
# print(get_best_rate('CommBank'))
# end = time.time()
# print(end - start)
# #print(get_best_rate('CommBank'))

# get_last_updated()

