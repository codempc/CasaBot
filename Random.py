import random
from response_text.show_rate import (
    BEST_RATE_RESPONSE_ONLY_BANK,
    BEST_RATE_RESPONSE_ONLY_REPAYMENT,
    BEST_RATE_RESPONSE_ONLY_FIXEDYEAR,
    BEST_RATE_RESPONSE_NO_INPUT,
    BEST_RATE_RESPONSE_ALL_INPUT,
    BEST_RATE_RESPONSE_BANK_MORTGAGE,
    BEST_RATE_RESPONSE_BANK_FIXEDYEAR,
    BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR,
)

from response_text.compare_rate import (
    COMPARE_RATE_RESPONSE_ALL_INPUT
)

from response_text.description import (
    DESC_IO,
    DESC_LVR,
    DESC_PI,
    NOT_UNDERSTAND
)

from response_text.best_compare_rate_followup import (
    BEST_COMPARE_FOLLOWUP_BETTER,
    BEST_COMPARE_FOLLOWUP_WORST
)


class Random:
    @staticmethod
    def get_resp_best_bank(params):

        if all(param == "" for param in params.values()):
            response_text = BEST_RATE_RESPONSE_NO_INPUT
        elif all(param != "" for param in params.values()):
            response_text = BEST_RATE_RESPONSE_ALL_INPUT
        elif params['bank'] != "" and params['mortgage'] != "":
            response_text = BEST_RATE_RESPONSE_BANK_MORTGAGE
        elif params['bank'] != "" and params['fixed_year'] != "":
            response_text = BEST_RATE_RESPONSE_BANK_FIXEDYEAR
        elif params['mortgage'] != "" and params['fixed_year'] != "":
            response_text = BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR
        elif params['bank'] != "":
            response_text = BEST_RATE_RESPONSE_ONLY_BANK
        elif params['mortgage'] != "":
            response_text = BEST_RATE_RESPONSE_ONLY_REPAYMENT
        elif params['fixed_year'] != "":
            response_text = BEST_RATE_RESPONSE_ONLY_FIXEDYEAR
        else:
            response_text = BEST_RATE_RESPONSE_NO_INPUT

        return response_text

    @staticmethod
    def best_bank(params, details):
        response_text = Random.get_resp_best_bank(params)

        output_string = random.choice(response_text)
        response = output_string.format(
            bank_name=details['bank_name'],
            interest_rate=details['interest_rate'],
            repayment_type=details['repayment_type'],
            year_fixed=details['year_fixed']
        )

        return response

    @staticmethod
    def get_resp_description(mortgage_type):
        if mortgage_type is None:
            return NOT_UNDERSTAND

        response_type = "DESC_"
        response_type += mortgage_type
        response_text = eval(response_type)
        print(response_text)

        return response_text

    @staticmethod
    def description(mortgage_type=None):
        response_type = Random.get_resp_description(mortgage_type)
        output_string = random.choice(response_type)
        response = output_string.format(
            mortgage_type=mortgage_type
        )

        return response

    # TODO: Compare Bank more response.
    @staticmethod
    def compare_bank(bank_1_details, bank_2_details):
        output_string = random.choice(COMPARE_RATE_RESPONSE_ALL_INPUT)
        # If interest_rate from bank 1 is higher
        if bank_1_details['interest_rate'] < bank_2_details['interest_rate']:
            response = output_string.format(
                bank_1=bank_1_details['bank_name'],
                bank_2=bank_2_details['bank_name'],
                repayment_type=bank_1_details['repayment_type'],
                year_fixed=bank_1_details['year_fixed'],
                rate_1=bank_1_details['interest_rate'],
                rate_2=bank_2_details['interest_rate'],
                diff_rate=round(bank_1_details['interest_rate'] - bank_2_details['interest_rate'], 2)
            )
        else:
            response = output_string.format(
                bank_1=bank_2_details['bank_name'],
                bank_2=bank_1_details['bank_name'],
                repayment_type=bank_2_details['repayment_type'],
                year_fixed=bank_2_details['year_fixed'],
                rate_1=bank_2_details['interest_rate'],
                rate_2=bank_1_details['interest_rate'],
                diff_rate=round(bank_2_details['interest_rate'] - bank_1_details['interest_rate'], 2)
            )
        return response

    @staticmethod
    def get_best_rate_compare_followup_resp(old_rate, best_rate):
        if old_rate > best_rate['interest_rate']:
            response_text = BEST_COMPARE_FOLLOWUP_BETTER
        else:
            response_text = BEST_COMPARE_FOLLOWUP_WORST
        return response_text

    @staticmethod
    def best_rate_compare_followup(old_rate, best_rate):
        response_text = Random.get_best_rate_compare_followup_resp(old_rate, best_rate)
        output_string = random.choice(response_text)
        if old_rate > best_rate['interest_rate']:
            response = output_string.format(
                bank_name=best_rate['bank_name'],
                old_rate=old_rate,
                new_rate=best_rate['interest_rate'],
                diff_rate=round(old_rate - best_rate['interest_rate'], 2)
            )
        else:
            response = output_string.format(
                bank_name=best_rate['bank_name'],
                old_rate=old_rate,
                new_rate=best_rate['interest_rate'],
                diff_rate=round(best_rate['interest_rate'] - old_rate, 2)
            )

        return response
