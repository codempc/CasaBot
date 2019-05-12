NO_INPUT = [
    'To give you a specific rate, I need you to tell me the bank name and the repayment type (IO/P&I)',
    'Please start by telling me the bank name and the repayment type (IO/P&I)',
    'Sure, what is the bank name and what is your type of repayment (IO/P&I)?'
]

ONLY_BANK = [
    'Cool! Rate for {bank_name}, next, tell me the type of repayment as well (IO/P&I)? ',
    '{bank_name}, Understood! Please tell me the type of repayment as well!',
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

BEST_RATE_RESPONSE_NO_INPUT = [
    'At the market, the lowest rate at the moment for home loan is {interest_rate}%. This rate is exclusively offered by'
    ' {bank_name}, with a repayment type of {repayment_type}, and year fixed rate of {year_fixed} years',
    'The lowest rate currently offered by the top banks in Australia is {interest_rate}%. You can get this lowest rate'
    ' if you apply the home loan program with {bank_name}. This program includes a repayment type of {repayment_type}'
    ' and the rate is fixed for {year_fixed} years.'
]

BEST_RATE_RESPONSE_ONLY_BANK = [
    'The best rate available at the moment for {bank_name} is {interest_rate}%.' 
    ' This program comes with a repayment type of {repayment_type} and it is fixed for {year_fixed} years',
    'The best rate we retrieved for {bank_name} is {interest_rate}%.'
    ' The repayment type is {repayment_type}, and this rate is fix for {year_fixed} years',
]

BEST_RATE_RESPONSE_ONLY_REPAYMENT = [
    'Best home loan rate for repayment type of {repayment_type} is {interest_rate}% from {bank_name} and fixed for {year_fixed} years',
    'Great choice! With mortgage type of {repayment_type}, the best rate available at the moment is {interest_rate}%, which'
    ' is offered by {bank_name} and this rate is fix for {year_fixed} years.'
]

BEST_RATE_RESPONSE_ONLY_FIXEDYEAR = [
    'For a rate that is fixed for {year_fixed} years, the best rate currently available is {interest_rate}%, offered by {bank_name}.',
    'Great! The best rate for a {year_fixed} year fixed program'
    ' available at the moment is {interest_rate}%. You can apply this via {bank_name}.'
    ' Also, by the way, this is for repayment type of {repayment_type}'
]

BEST_RATE_RESPONSE_BANK_MORTGAGE = [
    'That was a great choice! For Bank {bank_name} and repayment type of {repayment_type}, the best home loan rate is {interest_rate}%.'
    ' This rate is fixed for {year_fixed} years.',
    'Alrighty! With {bank_name} and the repayment_type of {repayment_type},'
    ' the best rate available is {interest_rate}% which is fixed for {fixed_year} years.',
]

BEST_RATE_RESPONSE_BANK_FIXEDYEAR = [
    'With a fixed year rate of {year_fixed}, Bank {bank_name} can offer you the lowest rate of {interest_rate}%' 
    ' if you apply for the repayment type: {repayment_type} program.',
    'Applying for the fixed year rate of {year_fixed} through {bank_name} can give you'
    ' the lowest rate of {interest_rate}% if you apply for the {repayment_type} program',
]

BEST_RATE_RESPONSE_MORTGAGE_FIXEDYEAR = [
    '{bank_name} has the best rate of {interest_rate}% for a program with mortgage type:' 
    ' {repayment_type} and fixed rate of {year_fixed} years.',
    'So, you want program {repayment_type} and fixed rate for {year_fixed} years.'
    ' If you apply through {bank_name}, you can get the lowest rate of {interest_rate}%'
]

BEST_RATE_RESPONSE_ALL_INPUT = [
    'The best rate for {bank_name} with a repayment type {repayment_type} and fixed year rate of {year_fixed} years is {interest_rate}%',
    'The best rate at the moment I can find: Bank Name: {bank_name}, Repayment Type: {repayment_type} Fixed year rate of {year_fixed} years is {interest_rate}%'
]

COMPARE_RATE_RESPONSE_ALL_INPUT = [
    'For a program with repayment type of {repayment_type} and fixed year rate of {year_fixed} years,'
    '{bank_1} can give a rate of {rate_1}%, while {bank_2} can give a rate of {rate_2}%',
    'With program for repayment type of {repayment_type} and fixed year rate of {year_fixed} years,'
    ' {bank_1}({rate_1}%) give a better rate than {bank_2}({rate_2}%) of {diff_rate}% '
]