# This is where we read data from googlesheet and then use that data for webhook.
import gspread
import pprint
import json
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate


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


def get_best_rate(bank_name="", amount="", time="", mortage_types=""):
    # TODO: Get the list of arrays from the read function from GoogleSheets.
    # TODO: Format data for the result should be in array like below
    #  (although in the real situation we should show more columns).
    result = [['CommBank', '4%'], ['Westpac', '3.8%'],
              ['St. George', '3.72%'], ['Suncorp', '3.34%'],
              ['ANZ', '3.28%']]

    table_card = {
        "tableCard": {
            "title": "AoG Table Card title",
            "subtitle": "AoG Table Card subtitle",
            "image": {
                "url": "",
                "accessibilityText": "Image description for screen readers"
            },
            "columnProperties": [
                {
                    "header": "Header 1"
                },
                {
                    "header": "Header 2",
                    "horizontalAlignment": "CENTER"
                },
                {
                    "header": "Header 3",
                    "horizontalAlignment": "CENTER"
                }
            ],
            "rows": [
                {
                    "cells": [
                        {
                            "text": "Cell A1"
                        },
                        {
                            "text": "Cell A2"
                        },
                        {
                            "text": "Cell A3"
                        },
                    ]
                },
                {
                    "cells": [
                        {
                            "text": "Cell B1"
                        },
                        {
                            "text": "Cell B2"
                        },
                        {
                            "text": "Cell B3"
                        }
                    ]
                },
                {
                    "cells": [
                        {
                            "text": "Cell C1"
                        },
                        {
                            "text": "Cell C2"
                        },
                        {
                            "text": "Cell C3"
                        }
                    ]
                }
            ],
            "buttons": [
                {
                    "title": "Button title",
                    "openUrlAction": {
                        "url": ""
                    }
                }
            ]
        }
    }
    my_result = {
        "fulfillmentText": "This is a text response",
        "fulfillmentMessages": [
            {
                "card": {
                    "title": "card title",
                    "subtitle": "card text",
                    "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                    "buttons": [
                        {
                            "text": "button text",
                            "postback": "https://assistant.google.com/"
                        }
                    ]
                }
            }
        ],
        "source": "example.com",
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "This is a simple table example."
                            }
                        },
                        {
                            "tableCard": {
                                "rows": [
                                    {
                                        "cells": [
                                            {
                                                "text": "row 1 item 1"
                                            },
                                            {
                                                "text": "row 1 item 2"
                                            },
                                            {
                                                "text": "row 1 item 3"
                                            }
                                        ],
                                        "dividerAfter": True
                                    },
                                    {
                                        "cells": [
                                            {
                                                "text": "row 2 item 1"
                                            },
                                            {
                                                "text": "row 2 item 2"
                                            },
                                            {
                                                "text": "row 2 item 3"
                                            }
                                        ],
                                        "dividerAfter": True
                                    }
                                ],
                                "columnProperties": [
                                    {
                                        "header": "header 1"
                                    },
                                    {
                                        "header": "header 2"
                                    },
                                    {
                                        "header": "header 3"
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            "facebook": table_card
        }
    }
    res = json.dumps(my_result, indent=4)
    result = tabulate(result, headers=['Bank', 'Rate'], tablefmt='orgtbl')
    return res


def view_all_data(file_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('bank_secret.json', scope)
    client = gspread.authorize(creds)

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
