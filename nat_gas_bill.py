import datetime as dt
import calendar

first_day = dt.date.fromisoformat('2024-10-14')
last_day = dt.date.today() # dt.datetime.now()
last_day =  dt.date.fromisoformat('2024-11-14')
number_of_days = (last_day - first_day).days

first_index = 7648 # cubic meter
last_index = 7679 # cubic meter
consumption_of_gas = last_index - first_index # cubic meter



def get_the_gas_bill(consumption_of_gas):
    correction_coefficient = 1.00089
    adjusted_consumption = consumption_of_gas * correction_coefficient


    actual_upper_calorific_value = 9396.0129 # kcal / cubic_meter
    a_kWh = 860.42 # kcal
    actual_upper_kWh_value = actual_upper_calorific_value / a_kWh

    amount_of_energy_consumed = adjusted_consumption * actual_upper_kWh_value

    retail_energy_price = 0.79297484
    consumption_cost = retail_energy_price * amount_of_energy_consumed

    tax_rate = 0.2
    cost_with_tax = consumption_cost * (1 + tax_rate)

    daily_consumption = cost_with_tax / number_of_days

    if number_of_days < 31:
        consumption_in_billing_period = daily_consumption * 30 # monthly consumption, 30 or 31 days in a month
    else:
        consumption_in_billing_period = daily_consumption * number_of_days


    daily_consumption_of_gas = consumption_of_gas / number_of_days
    monthly_consumption_of_gas = daily_consumption_of_gas * 30 # assume 30 days in a month

    print(f'Total Consumption as Price: {consumption_in_billing_period:.2f}' )


consumption_cost = get_the_gas_bill(consumption_of_gas)





