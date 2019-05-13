import random


def random_response_best_bank(response_type, details):
    output_string = random.choice(response_type)
    response = output_string.format(
        bank_name=details['bank_name'],
        interest_rate=details['interest_rate'],
        repayment_type=details['repayment_type'],
        year_fixed=details['year_fixed']
    )

    return response


def random_response_description(response_type, mortgage_type=None):
    output_string = random.choice(response_type)
    response = output_string.format(
        mortgage_type=mortgage_type
    )

    return response
