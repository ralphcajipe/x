# Cash in Python

"""
Note:
I decided not to use the get_float training wheel from cs50 module.
It's because I'm comfortable with Python's int and float data type.
"""

while True:
    try:
        # Ask how many dollars the customer is owed
        dollars = float(input("Change owed: "))

        # The next lines are my arithmetic logic to compute the...
        # minimum number of coins required to give a user change.

        # Calculate the number of quarters to give the customer
        quarters = int(dollars * 100) // 25

        # Calculate the number of dimes to give the customer
        dimes = int(dollars * 100) % 25 // 10

        # Calculate the number of nickels to give the customer
        nickels = int(dollars * 100) % 25 % 10 // 5

        # Calculate the number of pennies to give the customer
        pennies = int(dollars * 100) % 25 % 10 % 5

        if dollars < 0:
            # Reprompt
            continue
        elif dollars == "" or dollars == " ":
            # Reprompt
            continue
    except ValueError:
        # Reprompt if user inputs a non-negative value
        pass
    else:
        # Print total number of dollars to give the customer
        give_dollars = quarters + dimes + nickels + pennies
        print(give_dollars)
        break
