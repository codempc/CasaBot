NO_INPUT = [
    'To give you a rate, I need you to tell me the bank name, loan amount and loan year period',
    'Please start by telling me the bank name, loan amount and year period',
    'Sure, what is the bank name, loan amount and year period you want to apply this home loan for?'
]

ONLY_BANK = [
    'Cool! Rate for {bank_name}, next step is to specify the loan amount and year period for the '
    'home loan you want to apply for',
    '{bank_name}, Understood! Please tell me the loan amount and year period as well!',
    'Alrighty, next! Tell me the how much and how long do you want to loan.'
]

NO_BANK = [
    'Sure, first start with telling me the bank name!',
    'Okay, please tell me the bank name?',
    'Sure, next, please provide me with the bank name!'
]

NO_LOAN_AMOUNT = [
    'Okay! Rate for {bank_name}, please tell me the loan amount you want for',
    'Rate for {bank_name}, how much is your required loan amount?',
    'Please tell me how much do you want to loan for?'

]

NO_LOAN_PERIOD = [
    'Okay! Rate for {bank_name}, please tell me the loan period you want for',
    'Rate for {bank_name}, how long is this loan for?',
    'Okay, please tell me the duration of the loan as well'
]

SHOW_RATE_RESPONSE = [
    'The rate for {bank_name} with a loan amount of ${amount} and period of {time} {time_unit} is {rate}%',
    'Your rate for Bank Name: {bank_name}, Loan Amount: ${amount}, Loan Payment Period: {time} {time_unit} is {rate}%',
    'Understood! So you will be applying with {bank_name} needing about ${amount} '
    'and will be paying that after {time} {time_unit}. Rate: {rate}%'
]