import math

# user is allowed to choose which calculation they want
while True:
    calculation = input(
        "Choose either 'investment or 'bond' from the menu below to proceed: \n investment - to calculate the amount of interest you'll earn on your investment \n bond - to calculate the amount you'll have to pay on a home loan \n "
    ).lower()
    # when user selects investment, user is requested to provide deposit, interest rate, type of investment to determine accured amount
    if calculation == "investment":
        investment_deposit = float(input("How much are you depositing? "))
        investment_interest_rate = float(
            input("What is the interest rate (as a percentage)? ")
        )
        investment_years = float(
            input("How many years are you planning on investing for? ")
        )
        investment_type = input(
            "Do you want to simple or compound interest on your investment? "
        ).lower()
        # if investment type selected is simple;
        # investment_total is calculated with the formula; deposit * (1 + (interest_rate/100) * length of investment
        if investment_type == "simple" or "simple interest":
            investment_total = investment_deposit * (
                1 + (investment_interest_rate / 100) * investment_years
            )
            # print statement; round to nearest 2 sig fig
            print("You will accure {0:.2f}".format(investment_total))
            continue_ = input("Do you wish to continue? (Y/N) ").lower()
            if continue_ in ["y"]:
                continue
            else:
                break
        # if investment type selected is compound;
        # investment total is calculated with formula; deposit * ((1 + (interest_rate/100) ^ length))
        elif investment_type == "compound" or "compound interest":
            investment_total = investment_deposit * math(
                pow(1 + (investment_interest_rate / 100)), investment_years
            )
            # print statement; round to nearest 2 sig fig
            print("You will accure {0:.2f}".format(investment_total))
            continue_ = input("Do you wish to continue? (Y/N) ").lower()
            if continue_ in ["y"]:
                continue
            else:
                break
    # if user select bonds, user is requested to provide value, interest rate and length of repayment to determine the monthly repayment cost
    elif calculation == "bond":
        bond_value = float(input("What is the present value of the house? \n"))
        bond_interest_rate = float(input("What is the interest rate? \n"))
        # monthly interest rate is calculated by taking the annual interest rate and dividing it by 12
        monthly_interest_rate = (bond_interest_rate / 100) / 12
        bond_months = float(
            input("How many months do you plan to take to repay the bond? \n")
        )
        # repayment is calculated by (monthly interest . )
        repayment = float(
            (monthly_interest_rate * bond_value)
            / (1 - ((1 + monthly_interest_rate) ** (-bond_months)))
        )
        print("You will need to pay {0:.2f}".format(repayment))
        continue_ = input("Do you wish to continue? (Y/N) ").lower()
        if continue_ in ["y"]:
            continue
        else:
            break
    # if user does not select bond or investment, user restarts the program, otherwise user exits program
    else:
        print("You must select investment or bond. Please try again \n")
        continue_ = input("Do you wish to continue? (Y/N) ").lower()
        if continue_ in ["y"]:
            continue
        else:
            break
