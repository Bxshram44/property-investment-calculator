def calculate_gross_yield(annual_rent, property_price):
    gross_yield = (annual_rent / property_price) * 100
    return gross_yield
#"Def" creates functions
#Calculate_Gross_Field is the functions name
#Annual_rent , property_price = information that the function needs
#"return" = sends the calculated answer back.

def calculate_mortgage_payment(mortgage_amount, monthly_interest_rate, number_of_payments):
    monthly_payment = mortgage_amount * (
        monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments
    ) / (
        (1 + monthly_interest_rate) ** number_of_payments - 1
    )
    return monthly_payment

def calculate_cash_flow(monthly_rent, monthly_payment, monthly_expenses):
    monthly_cash_flow = monthly_rent - monthly_payment - monthly_expenses
    return monthly_cash_flow

def calculate_cash_on_cash_return(annual_cash_flow, total_cash_invested):
    cash_on_cash_return = (annual_cash_flow / total_cash_invested) * 100
    return cash_on_cash_return

def get_number(message):
    while True:
        try:
            number = float(input(message))
            return number
        except ValueError:
            print("Invalid input. Please enter a number.")
#Error Handling: keeps the loop going until successeful return
#float(input(message)) = tries to convert what the user entered into a number.
#except ValueError: = if that conversion fails, don't crash; run this instead.
#return number = sends the valid number back and automatically exits the function.

def calculate_interest_only_payment(mortgage_amount, interest_rate):
    monthly_payment = mortgage_amount * (interest_rate / 100) / 12
    return monthly_payment


print("Welcome to my Property Investment Calculator")
def analyse_property():
    property_price = get_number("Enter property price: £")

    while property_price <= 0:
        print("Property price must be greater than £0.")
        property_price = get_number("Enter property price again: £")

    deposit_percentage = get_number("Enter deposit percentage: ")

    while deposit_percentage <= 0 or deposit_percentage >= 100:
        print("Deposit percentage must be between 0 and 100.")
        deposit_percentage = get_number("Enter deposit percentage again: ")

    monthly_rent = get_number("Enter monthly rent: £")
    interest_rate = get_number("Enter annual interest rate (%): ")
    mortgage_years = get_number("Enter mortgage term (years): ")
    print("\nMortgage types:")
    print("1. Repayment")
    print("2. Interest-only")

    mortgage_type = get_number("Choose mortgage type (1 or 2): ")

    #"!" means Not equal to
    while mortgage_type != 1 and mortgage_type != 2:
        print("Please enter 1 or 2.")
        mortgage_type = get_number("Choose mortgage type (1 or 2): ")
    monthly_maintenance = get_number("Enter monthly maintenance cost: £")
    monthly_insurance = get_number("Enter monthly insurance cost: £")
    monthly_management = get_number("Enter monthly management cost: £")
    additional_costs = get_number("Enter additional purchase/renovation costs: £")

    annual_rent = monthly_rent * 12
    gross_yield = calculate_gross_yield(annual_rent, property_price)
    deposit_amount = (property_price * deposit_percentage)/100
    mortgage_amount = property_price - deposit_amount
    monthly_interest_rate = (interest_rate / 100) / 12
    number_of_payments = mortgage_years * 12
    monthly_expenses = monthly_maintenance + monthly_insurance + monthly_management
    if mortgage_type == 1:
        monthly_payment = calculate_mortgage_payment(
            mortgage_amount,
            monthly_interest_rate,
            number_of_payments
        )
    else:
        monthly_payment = calculate_interest_only_payment(
            mortgage_amount,
            interest_rate
        )
    monthly_cash_flow = calculate_cash_flow(
        monthly_rent,
        monthly_payment,
        monthly_expenses
    )

    annual_cash_flow = monthly_cash_flow * 12
    total_cash_invested = additional_costs + deposit_amount
    cash_on_cash_return = calculate_cash_on_cash_return(
        annual_cash_flow,
        total_cash_invested
    )

    property_data = {
        "price": property_price,
        "monthly_rent": monthly_rent,
        "gross_yield": gross_yield,
        "monthly_cash_flow": monthly_cash_flow,
        "cash_on_cash_return": cash_on_cash_return
    }
    print(property_data)

    print("Annual rent: £", annual_rent)
    print("Gross rental yield:", round(gross_yield, 2), "%")
    print("Deposit amount: £", deposit_amount)
    print("Mortgage amount: £", mortgage_amount)
    print("Monthly mortgage payment: £", round(monthly_payment, 2))
    print("Monthly cash flow: £", round(monthly_cash_flow, 2))
    print("Annual cash flow: £", round(annual_cash_flow, 2))
    print("Cash-on-cash return:", round(cash_on_cash_return, 2), "%")
    print("Total cash invested: £", round(total_cash_invested, 2))


    if gross_yield >= 7:
        print("High yield")
    elif gross_yield >= 5:
        print("Meets target")
    else:
        print("Below target")

    return property_data

properties = [] #creates empty lists for properties input

while True: #keeps repeating until it is instructed to stop
    property_data = analyse_property()
    properties.append(property_data)

    another_property = input(
        "\nWould you like to analyse another property? (yes/no): "
    ).lower()

    while another_property != "yes" and another_property != "no":
        print("Please enter yes or no.")
        another_property = input(
            "Would you like to analyse another property? (yes/no): "
        ).lower()

    if another_property == "no":
        break #tells loop to end


print("\n--- PROPERTY COMPARISON ---")

for index, property_data in enumerate(properties, start=1):
    print("\nProperty", index)
    print("Price: £", property_data["price"])
    print("Monthly rent: £", property_data["monthly_rent"])
    print("Gross yield:", round(property_data["gross_yield"], 2), "%")
    print("Monthly cash flow: £", round(property_data["monthly_cash_flow"], 2))
    print("Cash-on-cash return:", round(property_data["cash_on_cash_return"], 2), "%")
    #enumerate(properties, start=1) lets Python also keep count.
    #property_data["gross_yield"] reaches for the value stored in "Gross_yield" inside the properties dictionary

best_yield_property = max(properties, key=lambda property_data: property_data["gross_yield"])
best_cash_flow_property = max(properties, key=lambda property_data: property_data["monthly_cash_flow"])
#"key" tells python what value inside each dictionary it should compare.
print("\n--- BEST RESULTS ---")

print(
    "Highest gross yield:",
    round(best_yield_property["gross_yield"], 2),
    "%"
)

print(
    "Highest monthly cash flow: £",
    round(best_cash_flow_property["monthly_cash_flow"], 2)
)
