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
    BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR,
    COMPARE_RATE_RESPONSE_ALL_INPUT
)
from description_responses import (
    DESC_IO,
    DESC_LVR,
    DESC_PI,
    NOT_UNDERSTAND
)
from util import (
    random_response_best_bank,
    random_response_description
)

# Start Flask.
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
        response = random_response_description(DESC_IO, mortgage_type)
    elif mortgage_type == "P&I":
        response = random_response_description(DESC_PI, mortgage_type)
    elif mortgage_type == "LVR":
        response = random_response_description(DESC_LVR, mortgage_type)
    else:
        response = random_response_description(NOT_UNDERSTAND)
    return response


def get_parameters(req):
    return req['queryResult']['parameters']

def compare_rate(req):
    # TODO: Get the request and show right response.
    response = "The comparison ..."
    parameters = get_parameters(req)

    params = {
        "bank1": parameters['Australian_Banks'],
        "bank2": parameters['Australian_Banks1'],
        "mortgage": parameters['Mortgage_types'],
        "year_fixed": parameters['year_fixed']
    }

    best_rate_bank1 = get_best_rate(params["bank1"] or None, params["mortgage"] or None, params["year_fixed"] or None)
    best_rate_bank2 = get_best_rate(params["bank2"] or None, params["mortgage"] or None, params["year_fixed"] or None)

    if (all(param != "" for param in params.values())):
        output_string = random.choice(COMPARE_RATE_RESPONSE_ALL_INPUT)
        if (best_rate_bank1['interest_rate'] > best_rate_bank2['interest_rate']):
            response = output_string.format(
                bank_1=best_rate_bank1['bank_name'],
                bank_2=best_rate_bank2['bank_name'],
                repayment_type=params['mortgage'],
                year_fixed=params['year_fixed'],
                rate_1=best_rate_bank1['interest_rate'],
                rate_2=best_rate_bank2['interest_rate'],
                diff_rate=round(best_rate_bank1['interest_rate'] - best_rate_bank2['interest_rate'], 2)
            )
        else:
            response = output_string.format(
                bank_1=best_rate_bank2['bank_name'],
                bank_2=best_rate_bank1['bank_name'],
                repayment_type=params['mortgage'],
                year_fixed=params['year_fixed'],
                rate_1=best_rate_bank2['interest_rate'],
                rate_2=best_rate_bank1['interest_rate'],
                diff_rate=round(best_rate_bank2['interest_rate'] - best_rate_bank1['interest_rate'], 2)
            )
    return response


def best_rate(req):
    parameters = get_parameters(req)

    bank_param = parameters['Australian_Banks']
    mortgage_param = parameters['Mortgage_types']
    fixed_year_param = parameters['fixed_year']

    params = {
        "bank_param": parameters['Australian_Banks'],
        "mortgage_param": parameters['Mortgage_types'],
        "fixed_year_param": parameters['fixed_year']
    }

    best_rate = get_best_rate(bank_param or None, mortgage_param or None, fixed_year_param or None)

    response_text = None

    if (all(param == "" for param in params.values())):
        response_text = BEST_RATE_RESPONSE_NO_INPUT
    elif (all(param != "" for param in params.values())):
        response_text = BEST_RATE_RESPONSE_ALL_INPUT
    elif bank_param != "" and mortgage_param != "":
        response_text =  BEST_RATE_RESPONSE_BANK_MORTGAGE
    elif bank_param != "" and fixed_year_param != "":
        response_text = BEST_RATE_RESPONSE_BANK_FIXEDYEAR
    elif mortgage_param != "" and fixed_year_param != "":
        response_text = BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR
    elif bank_param != "":
        response_text = BEST_RATE_RESPONSE_ONLY_BANK
    elif mortgage_param != "":
        response_text = BEST_RATE_RESPONSE_ONLY_REPAYMENT
    elif fixed_year_param != "":
        response_text = BEST_RATE_RESPONSE_ONLY_FIXEDYEAR
    else:
        response_text = BEST_RATE_RESPONSE_NO_INPUT
    
    response = random_response_best_bank(response_text, best_rate)

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
