import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
import seaborn as sns

#remaining mortgage balance
addtl_pp = 5000
loan_lnsb = 701670.05
loan_rio = 0
rmb = loan_lnsb + loan_rio
mortgage_Loan = 1200000

years = 10
mortgage_payment_periods = years * 12
annual_rate = 0.08

#mortage interest rate (periodic)
r = (1 + annual_rate)**(1/12) -1
mp = npf.pmt(rate=r, nper=mortgage_payment_periods, pv=rmb)
#mortgage payment

#interest payment
ip = rmb * r
#principal payment
pp = -mp - ip


print('interest payment: '+ str(ip))
print('principal payment: '+ str(pp))
print(ip+pp)

interest_paid =[]
principal_paid = []
principal_remaining = []
for i in range(0, mortgage_payment_periods):
    principal_remaining.append(0)
    interest_paid.append(0)
    principal_paid.append(0)

# Loop through each mortgage payment period
for i in range(0, mortgage_payment_periods):

    # Handle the case for the first iteration
    if i == 0:
        previous_principal_remaining = rmb
    else:
        previous_principal_remaining = principal_remaining[i - 1]

    # Calculate the interest based on the previous principal
    interest_payment = round(previous_principal_remaining * r, 2)
    principal_payment = round(-mp - interest_payment + addtl_pp, 2)

    # Catch the case where all principal is paid off in the final period
    if previous_principal_remaining - principal_payment < 0:
        principal_payment = previous_principal_remaining

    # Collect the historical values
    interest_paid[i] = interest_payment
    principal_paid[i] = principal_payment
    principal_remaining[i] = previous_principal_remaining - principal_payment

# Plot the interest vs principal
plt.clf()
sns.set_context("talk")
p1 = sns.lineplot(interest_paid, color="red", label='interest_paid')
p2 = sns.lineplot(principal_paid, color="blue", label='principal_paid')
plt.ylabel('Payment')
plt.xlabel('Month')
plt.suptitle("Interest vs Principal Payments Over Time")
plt.title('(addtl 5k payment to principal at 8% annual rate)',\
          fontweight='bold',\
          style='italic')

plt.show()

amortization_schedule = pd.DataFrame(list(zip(interest_paid, principal_paid, principal_remaining)), columns=['interest_paid', 'principal_paid', 'principal_remaining'])
