# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

import random

from flask import Flask, request, make_response, jsonify
from GoogleSheet.read import get_rate, get_best_rate
from show_rate_responses import (
    NO_INPUT,
    NO_BANK,
    NO_LOAN_AMOUNT,
    NO_LOAN_PERIOD,
    ONLY_BANK
)

# Flask app should start in global layout
app = Flask(__name__)
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    try:
        intent = req.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        return 'json error'

    print('Intent: ' + intent)
    if intent == 'showRate':
        res = show_rate(req)
    elif intent == 'description':
        res = description(req)
    elif intent == 'compareRate':
        res = compare_rate(req)
    elif intent == 'bestRate':
        res = best_rate(req)
    elif intent == 'rate-followup':
        res = rate_followup(req)
    else:
        # TODO: Fix the else statement for res with fallback intent?
        res = show_rate(req)

    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return make_response(jsonify({'fulfillmentText': res}))


def description(req):
    parameters = req['queryResult']['parameters']

    mortgage_type = parameters["Mortgage_types"]
    if mortgage_type == "IO":
        response = mortgage_type + " or Interest Only loan is a loan in which " \
                                   "the borrower pays only the interest for some or all of the " \
                                   "term, with the principal balance unchanged during the interest-only period."
    elif mortgage_type == "P&I":
        response = mortgage_type + " or Principal and Interest loan is a loan in which " \
                                   "the borrower pays the portioon of principal with " \
                                   "the interest in a certain period of time."
    elif mortgage_type == "LVR":
        response = mortgage_type + " or Loan to Value Ratio is calculated by dividing the loan amount " \
                                   "by the actual purchase price or valuation of the property, then" \
                                   " multiplying it by 100."
    else:
        response = "Sorry, I do not understand what you mean."
    return response


def get_parameters(req):
    return req['queryResult']['parameters']


def show_rate(req):
    # Parsing the POST request body into a dictionary for easy access.
    intent_name = req['queryResult']['intent']['displayName']
    parameters = get_parameters(req)
    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))
    print("intent name:", intent_name)

    # if the name of the bank is not given, then tell
    # them that they need to include the name of the bank.
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    loan_amount = parameters["loan_value"]
    loan_year_period = parameters["loan_year_period"]
    bank_name = parameters['Australian_Banks']

    if bank_name == "" and loan_amount == "" and loan_year_period == "":
        response = random.choice(NO_INPUT)
    elif bank_name == "" and (loan_amount != "" or loan_year_period != ""):
        response = random.choice(NO_BANK)
    elif loan_amount == "" and loan_year_period == "":
        output_string = random.choice(ONLY_BANK)
        response = output_string.format(
            bank_name=bank_name
        )
    elif loan_amount == "":
        output_string = random.choice(NO_LOAN_AMOUNT)
        response = output_string.format(
            bank_name=bank_name
        )
    elif loan_year_period == "":
        output_string = random.choice(NO_LOAN_PERIOD)
        response = output_string.format(
            bank_name=bank_name
        )
    else:
        response = get_rate(bank_name, loan_amount, loan_year_period)
    return response


def compare_rate(req):
    # TODO: Get the request and show right response.
    response = "The comparison ..."
    return response


def best_rate(req):
    # TODO: Get the request as parameter and show right response.
    bank_name = None
    mortgage_type = None
    year_fixed = None

    parameters = get_parameters(req)

    if parameters['Australian_Banks'] != "":
        bank_name = parameters['Australian_Banks']

    if parameters['Mortgage_types'] != "":
        mortgage_type = parameters['Mortgage_types']

    if parameters['fixed_year'] != "":
        year_fixed = parameters['fixed_year']

    response = get_best_rate(bank_name, mortgage_type, year_fixed)
    return response


def rate_followup(req):
    parameters = get_parameters(req)
    bank_name = ""
    loan_amount = ""
    loan_year_period = ""
    if parameters["Australian_Banks"] != "":
        bank_name = parameters["Australian_Banks"]

    if parameters["loan_value"] != "":
        loan_amount = parameters["loan_value"]

    if parameters["loan_year_period"] != "":
        loan_year_period = parameters["loan_year_period"]

    response = get_rate(bank_name, loan_amount, loan_year_period)
    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
