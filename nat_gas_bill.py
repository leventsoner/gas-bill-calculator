import datetime as dt
from dataclasses import dataclass

@dataclass
class GasConstants:
    CORRECTION_COEFFICIENT = 1.00089
    ACTUAL_UPPER_CALORIFIC_VALUE = 9396.0129  # kcal/cubic_meter
    KCAL_PER_KWH = 860.42
    RETAIL_ENERGY_PRICE = 0.797288
    TAX_RATE = 0.2
    STANDARD_MONTH_DAYS = 30

def calculate_gas_bill(first_index: float, last_index: float, 
                      start_date: dt.date, end_date: dt.date) -> dict:
    """
    Calculate natural gas bill based on meter readings and dates.
    
    Args:
        first_index: Initial meter reading in cubic meters
        last_index: Final meter reading in cubic meters
        start_date: Start date of billing period
        end_date: End date of billing period
    
    Returns:
        dict: Dictionary containing consumption and cost details
    """
    if end_date <= start_date:
        raise ValueError("End date must be after start date")
    if last_index < first_index:
        raise ValueError("Final meter reading must be greater than initial reading")

    # Calculate basic consumption
    consumption_of_gas = last_index - first_index
    number_of_days = (end_date - start_date).days

    # Calculate daily and projected monthly consumption
    daily_consumption_m3 = consumption_of_gas / number_of_days
    monthly_consumption_m3 = daily_consumption_m3 * GasConstants.STANDARD_MONTH_DAYS

    # Convert volume to energy
    adjusted_consumption = consumption_of_gas * GasConstants.CORRECTION_COEFFICIENT
    actual_upper_kwh_value = GasConstants.ACTUAL_UPPER_CALORIFIC_VALUE / GasConstants.KCAL_PER_KWH
    amount_of_energy_consumed = adjusted_consumption * actual_upper_kwh_value

    # Calculate costs
    base_cost = amount_of_energy_consumed * GasConstants.RETAIL_ENERGY_PRICE
    total_cost = base_cost * (1 + GasConstants.TAX_RATE)
    daily_cost = total_cost / number_of_days
    
    # Project monthly bill
    projected_monthly_cost = daily_cost * GasConstants.STANDARD_MONTH_DAYS

    return {
        'consumption_m3': consumption_of_gas,
        'daily_consumption_m3': daily_consumption_m3,
        'monthly_projected_consumption_m3': monthly_consumption_m3,
        'energy_consumed_kwh': amount_of_energy_consumed,
        'daily_cost': daily_cost,
        'projected_monthly_cost': projected_monthly_cost,
        'total_cost_for_period': total_cost
    }

def get_date_input(prompt: str) -> dt.date:
    """Get and validate date input from user."""
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ")
            return dt.date.fromisoformat(date_str)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")

def get_float_input(prompt: str) -> float:
    """Get and validate float input from user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    print("\nNatural Gas Bill Calculator")
    print("-" * 30)
    
    # Get date inputs
    print("\nEnter the billing period dates:")
    first_day = get_date_input("Start date")
    last_day = get_date_input("End date")

    # Get meter readings
    print("\nEnter the meter readings (in cubic meters):")
    first_index = get_float_input("Initial meter reading: ")
    last_index = get_float_input("Final meter reading: ")

    try:
        result = calculate_gas_bill(first_index, last_index, first_day, last_day)
        
        print("\nNatural Gas Bill Calculation")
        print("-" * 30)
        print(f"Period: {first_day} to {last_day}")
        print(f"Consumption: {result['consumption_m3']:.2f} m³")
        print(f"Daily consumption: {result['daily_consumption_m3']:.2f} m³")
        print(f"Energy consumed: {result['energy_consumed_kwh']:.2f} kWh")
        print(f"Daily cost: €{result['daily_cost']:.2f}")
        print(f"Projected monthly bill: €{result['projected_monthly_cost']:.2f}")
        print(f"Total cost for period: €{result['total_cost_for_period']:.2f}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()





