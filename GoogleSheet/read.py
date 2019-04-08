# This is where we read data from googlesheet and then use that data for webhook.
def get_rate(bank_name, amount, time):
    # TODO: Get data from GoogleSheets.
    rate = "4.8%"  # Get from googlesheets based on the condition (bank_name, amount, time)

    # IF no loan amount and time, just give the first row while also giving the details. i.e.
    if amount == "":
        amount = "$40000"  # Get data from googlesheets first row for amount
    if time == "":
        time = "30 years"  # Get data from googlesheets first row for time

    return "The rate for " + bank_name + " with a loan amount of " + amount + " and year period of " + time + " is " + rate
