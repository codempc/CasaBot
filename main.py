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
from GoogleSheet.read import get_best_rate
from show_rate_responses import (
    NO_INPUT,
    NO_BANK,
    NO_LOAN_AMOUNT,
    NO_LOAN_PERIOD,
    ONLY_BANK,
    BEST_RATE_RESPONSE_ONLY_BANK,
    BEST_RATE_RESPONSE_ONLY_REPAYMENT,
    BEST_RATE_RESPONSE_ONLY_FIXEDYEAR,
    BEST_RATE_RESPONSE_NO_INPUT,
    BEST_RATE_RESPONSE_ALL_INPUT,
    BEST_RATE_RESPONSE_BANK_MORTGAGE,
    BEST_RATE_RESPONSE_BANK_FIXEDYEAR,
    BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR
)

from util import random_response_best_bank

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
    if intent == 'description':
        res = description(req)
    elif intent == 'compareRate':
        res = compare_rate(req)
    elif intent == 'bestRate':
        res, outputContexts = best_rate(req)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return make_response(jsonify({'fulfillmentText': res, 'outputContexts': [outputContexts]}))
    elif intent == 'rate-followup':
        res = rate_followup(req)
    else:
        # TODO: Fix the else statement for res with fallback intent?
        res = best_rate(req)

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

def compare_rate(req):
    # TODO: Get the request and show right response.
    response = "The comparison ..."
    return response


def best_rate(req):
    bank_name = None
    mortgage_type = None
    year_fixed = None

    parameters = get_parameters(req)

    bank_param = parameters['Australian_Banks']
    mortgage_param = parameters['Mortgage_types']
    fixed_year_param = parameters['fixed_year']

    params = {
        bank_param: parameters['Australian_Banks'],
        mortgage_param: parameters['Mortgage_types'],
        fixed_year_param: parameters['fixed_year']
    }

    if bank_param == "" and mortgage_param == "" and fixed_year_param == "":
        best_rate = get_best_rate(bank_name, mortgage_type, year_fixed)
        response = random_response_best_bank(BEST_RATE_RESPONSE_NO_INPUT, best_rate)
    elif bank_param != "" and mortgage_param != "" and fixed_year_param != "":
        best_rate = get_best_rate(bank_param, mortgage_param, fixed_year_param)
        response = random_response_best_bank(BEST_RATE_RESPONSE_ALL_INPUT, best_rate)
    elif bank_param != "" and mortgage_param != "":
        best_rate = get_best_rate(bank_param, mortgage_param, year_fixed)
        response = random_response_best_bank(BEST_RATE_RESPONSE_BANK_MORTGAGE, best_rate)
    elif bank_param != "" and fixed_year_param != "":
        best_rate = get_best_rate(bank_param, mortgage_type, fixed_year_param)
        response = random_response_best_bank(BEST_RATE_RESPONSE_BANK_FIXEDYEAR, best_rate)
    elif mortgage_param != "" and fixed_year_param != "":
        best_rate = get_best_rate(bank_name, mortgage_param, fixed_year_param)
        response = random_response_best_bank(BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR, best_rate)
    elif bank_param != "":
        best_rate = get_best_rate(bank_param, mortgage_type, year_fixed)
        response = random_response_best_bank(BEST_RATE_RESPONSE_ONLY_BANK, best_rate)
    elif mortgage_param != "":
        best_rate = get_best_rate(bank_name, mortgage_param, year_fixed)
        response = random_response_best_bank(BEST_RATE_RESPONSE_ONLY_REPAYMENT, best_rate)
    elif fixed_year_param != "":
        best_rate = get_best_rate(bank_name, mortgage_type, fixed_year_param)
        response = random_response_best_bank(BEST_RATE_RESPONSE_ONLY_FIXEDYEAR, best_rate)
    else:
        best_rate = get_best_rate(bank_param, mortgage_param, fixed_year_param)
        response = random_response_best_bank(BEST_RATE_RESPONSE_ALL_INPUT, best_rate)

    outputContexts = {
        "name": "projects/ron-anpelr/agent/sessions/e1dc138a-9f22-7941-80de-8998ede6221b/contexts/showrate-followup",
        "lifespanCount": 5,
        "parameters": {
            "fixed_year": best_rate['year_fixed'],
            "Australian_Banks": best_rate['bank_name'],
            "repayment_type": best_rate['repayment_type']
        }
    }

    return response, outputContexts


def rate_followup(req):
    parameters = get_parameters(req)
    bank_name = ""
    repayment_type = ""
    fixed_year = ""
    if parameters["Australian_Banks"] != "":
        bank_name = parameters["Australian_Banks"]
    if parameters["repayment_type"] != "":
        repayment_type = parameters["repayment_type"]
    if parameters["fixed_year"] != "":
        fixed_year = parameters["fixed_year"]

    best_rate = get_best_rate(bank_name, repayment_type, fixed_year)
    response = random_response_best_bank(BEST_RATE_RESPONSE_ALL_INPUT, best_rate)

    return response


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
