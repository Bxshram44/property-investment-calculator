import streamlit as st


# --------------------------------------------------
# CALCULATION FUNCTIONS
# --------------------------------------------------

def calculate_gross_yield(annual_rent, property_price):
    return (annual_rent / property_price) * 100


def calculate_mortgage_payment(
    mortgage_amount,
    monthly_interest_rate,
    number_of_payments
):
    # Prevent division-by-zero when interest rate is 0%
    if monthly_interest_rate == 0:
        return mortgage_amount / number_of_payments

    monthly_payment = mortgage_amount * (
        monthly_interest_rate
        * (1 + monthly_interest_rate) ** number_of_payments
    ) / (
        (1 + monthly_interest_rate) ** number_of_payments - 1
    )

    return monthly_payment


def calculate_interest_only_payment(
    mortgage_amount,
    interest_rate
):
    return mortgage_amount * (interest_rate / 100) / 12


def calculate_cash_flow(
    monthly_rent,
    monthly_payment,
    monthly_expenses
):
    return monthly_rent - monthly_payment - monthly_expenses


def calculate_cash_on_cash_return(
    annual_cash_flow,
    total_cash_invested
):
    if total_cash_invested == 0:
        return 0

    return (annual_cash_flow / total_cash_invested) * 100


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Property Investment Calculator",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Property Investment Calculator")

st.write(
    "Analyse the potential rental yield, cash flow and "
    "cash-on-cash return of a property investment."
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

# Stores properties saved for comparison
if "properties" not in st.session_state:
    st.session_state.properties = []

# Stores the most recently calculated property
if "current_property" not in st.session_state:
    st.session_state.current_property = None


# --------------------------------------------------
# PROPERTY DETAILS
# --------------------------------------------------

st.header("Property Details")

property_col1, property_col2 = st.columns(2)

with property_col1:
    property_price = st.number_input(
        "Property Price (£)",
        min_value=0.0,
        step=1000.0
    )

with property_col2:
    deposit_percentage = st.number_input(
        "Deposit Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )

monthly_rent = st.number_input(
    "Monthly Rent (£)",
    min_value=0.0,
    step=50.0
)


# --------------------------------------------------
# MORTGAGE DETAILS
# --------------------------------------------------

st.header("Mortgage Details")

mortgage_col1, mortgage_col2 = st.columns(2)

with mortgage_col1:
    interest_rate = st.number_input(
        "Annual Interest Rate (%)",
        min_value=0.0,
        step=0.1
    )

with mortgage_col2:
    mortgage_years = st.number_input(
        "Mortgage Term (Years)",
        min_value=1,
        max_value=50,
        step=1
    )

mortgage_type = st.selectbox(
    "Mortgage Type",
    ["Repayment", "Interest-only"]
)


# --------------------------------------------------
# EXPENSES
# --------------------------------------------------

st.header("Expenses")

expense_col1, expense_col2 = st.columns(2)

with expense_col1:
    monthly_maintenance = st.number_input(
        "Monthly Maintenance Cost (£)",
        min_value=0.0,
        step=10.0
    )

with expense_col2:
    monthly_insurance = st.number_input(
        "Monthly Insurance Cost (£)",
        min_value=0.0,
        step=10.0
    )

expense_col3, expense_col4 = st.columns(2)

with expense_col3:
    monthly_management = st.number_input(
        "Monthly Management Cost (£)",
        min_value=0.0,
        step=10.0
    )

with expense_col4:
    additional_costs = st.number_input(
        "Additional Purchase / Renovation Costs (£)",
        min_value=0.0,
        step=100.0
    )


# --------------------------------------------------
# CALCULATE BUTTON
# --------------------------------------------------

calculate_button = st.button(
    "Calculate Investment",
    type="primary"
)


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

if calculate_button:

    if property_price <= 0:
        st.error(
            "Please enter a property price greater than £0."
        )

    elif deposit_percentage <= 0:
        st.error(
            "Please enter a deposit percentage greater than 0%."
        )

    elif deposit_percentage >= 100:
        st.error(
            "Deposit percentage must be below 100%."
        )

    else:

        annual_rent = monthly_rent * 12

        gross_yield = calculate_gross_yield(
            annual_rent,
            property_price
        )

        deposit_amount = (
            property_price * deposit_percentage
        ) / 100

        mortgage_amount = (
            property_price - deposit_amount
        )

        monthly_interest_rate = (
            interest_rate / 100
        ) / 12

        number_of_payments = (
            mortgage_years * 12
        )

        monthly_expenses = (
            monthly_maintenance
            + monthly_insurance
            + monthly_management
        )

        if mortgage_type == "Repayment":
            monthly_payment = calculate_mortgage_payment(
                mortgage_amount,
                monthly_interest_rate,
                number_of_payments
            )

        else:
            monthly_payment = (
                calculate_interest_only_payment(
                    mortgage_amount,
                    interest_rate
                )
            )

        monthly_cash_flow = calculate_cash_flow(
            monthly_rent,
            monthly_payment,
            monthly_expenses
        )

        annual_cash_flow = (
            monthly_cash_flow * 12
        )

        total_cash_invested = (
            deposit_amount + additional_costs
        )

        cash_on_cash_return = (
            calculate_cash_on_cash_return(
                annual_cash_flow,
                total_cash_invested
            )
        )

        # Save the latest calculation
        st.session_state.current_property = {
            "price": property_price,
            "deposit_percentage": deposit_percentage,
            "monthly_rent": monthly_rent,
            "interest_rate": interest_rate,
            "mortgage_years": mortgage_years,
            "mortgage_type": mortgage_type,
            "annual_rent": annual_rent,
            "deposit_amount": deposit_amount,
            "mortgage_amount": mortgage_amount,
            "monthly_payment": monthly_payment,
            "monthly_expenses": monthly_expenses,
            "gross_yield": gross_yield,
            "monthly_cash_flow": monthly_cash_flow,
            "annual_cash_flow": annual_cash_flow,
            "total_cash_invested": total_cash_invested,
            "cash_on_cash_return": cash_on_cash_return
        }


# --------------------------------------------------
# CURRENT RESULTS
# --------------------------------------------------

if st.session_state.current_property is not None:

    property_data = st.session_state.current_property

    st.divider()

    st.header("Investment Results")

    result_col1, result_col2, result_col3, result_col4 = (
        st.columns(4)
    )

    with result_col1:
        st.metric(
            "Gross Rental Yield",
            f"{property_data['gross_yield']:.2f}%"
        )

    with result_col2:
        st.metric(
            "Monthly Cash Flow",
            f"£{property_data['monthly_cash_flow']:,.2f}"
        )

    with result_col3:
        st.metric(
            "Annual Cash Flow",
            f"£{property_data['annual_cash_flow']:,.2f}"
        )

    with result_col4:
        st.metric(
            "Cash-on-Cash Return",
            f"{property_data['cash_on_cash_return']:.2f}%"
        )


    # --------------------------------------------------
    # INVESTMENT BREAKDOWN
    # --------------------------------------------------

    st.subheader("Investment Breakdown")

    breakdown_col1, breakdown_col2 = st.columns(2)

    with breakdown_col1:

        st.write(
            f"**Annual Rent:** "
            f"£{property_data['annual_rent']:,.2f}"
        )

        st.write(
            f"**Deposit Amount:** "
            f"£{property_data['deposit_amount']:,.2f}"
        )

        st.write(
            f"**Mortgage Amount:** "
            f"£{property_data['mortgage_amount']:,.2f}"
        )

    with breakdown_col2:

        st.write(
            f"**Monthly Mortgage Payment:** "
            f"£{property_data['monthly_payment']:,.2f}"
        )

        st.write(
            f"**Monthly Expenses:** "
            f"£{property_data['monthly_expenses']:,.2f}"
        )

        st.write(
            f"**Total Cash Invested:** "
            f"£{property_data['total_cash_invested']:,.2f}"
        )


    # --------------------------------------------------
    # YIELD RATING
    # --------------------------------------------------

    st.subheader("Yield Rating")

    if property_data["gross_yield"] >= 7:
        st.success("High Yield")

    elif property_data["gross_yield"] >= 5:
        st.info("Meets Target")

    else:
        st.warning("Below Target")


    # --------------------------------------------------
    # ADD PROPERTY
    # --------------------------------------------------

    if st.button("Add Property to Comparison"):

        # Copy prevents later calculations from changing
        # a previously saved property.
        saved_property = property_data.copy()

        st.session_state.properties.append(
            saved_property
        )

        st.success(
            f"Property {len(st.session_state.properties)} "
            "added to comparison!"
        )


# --------------------------------------------------
# PROPERTY COMPARISON
# --------------------------------------------------

if len(st.session_state.properties) > 0:

    st.divider()

    st.header("Property Comparison")

    comparison_data = []

    for index, property_data in enumerate(
        st.session_state.properties,
        start=1
    ):

        comparison_data.append({
            "Property": f"Property {index}",
            "Price (£)": property_data["price"],
            "Monthly Rent (£)": property_data["monthly_rent"],
            "Gross Yield (%)": round(
                property_data["gross_yield"],
                2
            ),
            "Monthly Cash Flow (£)": round(
                property_data["monthly_cash_flow"],
                2
            ),
            "Cash-on-Cash Return (%)": round(
                property_data["cash_on_cash_return"],
                2
            )
        })

    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # BEST RESULTS
    # --------------------------------------------------

    st.subheader("Best Results")

    best_yield_index = max(
        range(len(st.session_state.properties)),
        key=lambda index:
        st.session_state.properties[index]["gross_yield"]
    )

    best_cash_flow_index = max(
        range(len(st.session_state.properties)),
        key=lambda index:
        st.session_state.properties[index]["monthly_cash_flow"]
    )

    best_return_index = max(
        range(len(st.session_state.properties)),
        key=lambda index:
        st.session_state.properties[index][
            "cash_on_cash_return"
        ]
    )

    best_col1, best_col2, best_col3 = st.columns(3)

    with best_col1:

        best_property = (
            st.session_state.properties[
                best_yield_index
            ]
        )

        st.metric(
            f"Best Gross Yield — Property "
            f"{best_yield_index + 1}",
            f"{best_property['gross_yield']:.2f}%"
        )

    with best_col2:

        best_property = (
            st.session_state.properties[
                best_cash_flow_index
            ]
        )

        st.metric(
            f"Best Cash Flow — Property "
            f"{best_cash_flow_index + 1}",
            f"£{best_property['monthly_cash_flow']:,.2f}"
        )

    with best_col3:

        best_property = (
            st.session_state.properties[
                best_return_index
            ]
        )

        st.metric(
            f"Best Cash-on-Cash Return — Property "
            f"{best_return_index + 1}",
            f"{best_property['cash_on_cash_return']:.2f}%"
        )


    # --------------------------------------------------
    # REMOVE / CLEAR PROPERTIES
    # --------------------------------------------------

    st.subheader("Manage Comparison")

    property_to_remove = st.selectbox(
        "Select a property to remove",
        range(1, len(st.session_state.properties) + 1),
        format_func=lambda number: f"Property {number}"
    )

    remove_col1, remove_col2 = st.columns(2)

    with remove_col1:

        if st.button("Remove Selected Property"):

            st.session_state.properties.pop(
                property_to_remove - 1
            )

            st.rerun()

    with remove_col2:

        if st.button("Clear All Properties"):

            st.session_state.properties = []

            st.rerun()


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.divider()

st.caption(
    "This calculator provides illustrative estimates only "
    "and is not financial advice."
)