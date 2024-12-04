import datetime as dt
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class GasConstants:
    CORRECTION_COEFFICIENT = 1.00089
    ACTUAL_UPPER_CALORIFIC_VALUE = 9396.0129  # kcal/cubic_meter
    KCAL_PER_KWH = 860.42
    RETAIL_ENERGY_PRICE = 0.797288
    TAX_RATE = 0.2
    STANDARD_MONTH_DAYS = 30

class Currency:
    SYMBOL = "€"  # Can be changed to "₺" for Turkish Lira
    POSITION = "before"  # or "after" for Turkish style

# Language dictionaries
LANGUAGES = {
    "en": {
        "title": "Natural Gas Bill Calculator",
        "enter_dates": "Enter the billing period dates:",
        "start_date": "Start date",
        "end_date": "End date",
        "enter_readings": "Enter the meter readings (in cubic meters):",
        "initial_reading": "Initial meter reading",
        "final_reading": "Final meter reading",
        "calculation_title": "Natural Gas Bill Calculation",
        "period": "Period",
        "consumption": "Consumption",
        "daily_consumption": "Daily consumption",
        "energy_consumed": "Energy consumed",
        "daily_cost": "Daily cost",
        "projected_monthly": "Projected monthly bill",
        "total_cost": "Total cost for period",
        "invalid_date": "Invalid date format. Please use YYYY-MM-DD format.",
        "invalid_number": "Invalid input. Please enter a number.",
        "negative_value": "Value cannot be negative.",
        "date_error": "End date must be after start date",
        "reading_error": "Final meter reading must be greater than initial reading"
    },
    "tr": {
        "title": "Doğal Gaz Fatura Hesaplayıcı",
        "enter_dates": "Fatura dönemi tarihlerini giriniz:",
        "start_date": "Başlangıç tarihi",
        "end_date": "Bitiş tarihi",
        "enter_readings": "Sayaç okumalarını giriniz (metreküp cinsinden):",
        "initial_reading": "İlk sayaç okuması",
        "final_reading": "Son sayaç okuması",
        "calculation_title": "Doğal Gaz Fatura Hesaplaması",
        "period": "Dönem",
        "consumption": "Tüketim",
        "daily_consumption": "Günlük tüketim",
        "energy_consumed": "Tüketilen enerji",
        "daily_cost": "Günlük maliyet",
        "projected_monthly": "Tahmini aylık fatura",
        "total_cost": "Dönem toplam maliyet",
        "invalid_date": "Geçersiz tarih formatı. Lütfen GG-AA-YYYY formatını kullanın.",
        "invalid_number": "Geçersiz giriş. Lütfen bir sayı girin.",
        "negative_value": "Değer negatif olamaz.",
        "date_error": "Bitiş tarihi başlangıç tarihinden sonra olmalıdır",
        "reading_error": "Son sayaç okuması ilk okumadan büyük olmalıdır"
    }
}

def format_currency(amount: float, language: str) -> str:
    """Format currency according to locale preferences."""
    if Currency.POSITION == "before":
        return f"{Currency.SYMBOL}{amount:.2f}"
    return f"{amount:.2f}{Currency.SYMBOL}"

def calculate_gas_bill(first_index: float, last_index: float, 
                      start_date: dt.date, end_date: dt.date,
                      lang: str = "en") -> dict:
    """Calculate natural gas bill (same as before but with language parameter)"""
    if end_date <= start_date:
        raise ValueError(LANGUAGES[lang]["date_error"])
    if last_index < first_index:
        raise ValueError(LANGUAGES[lang]["reading_error"])
    
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

def get_date_input(prompt: str, lang: str) -> dt.date:
    """Get and validate date input from user."""
    while True:
        try:
            if lang == "tr":
                date_str = input(f"{prompt} (GG-AA-YYYY): ")
                if "-" in date_str:
                    day, month, year = map(int, date_str.split("-"))
                    return dt.date(year, month, day)
            else:
                date_str = input(f"{prompt} (YYYY-MM-DD): ")
                return dt.date.fromisoformat(date_str)
        except (ValueError, TypeError):
            if lang == "tr":
                print(LANGUAGES[lang]["invalid_date"])
            else:
                print(LANGUAGES[lang]["invalid_date"])

def get_float_input(prompt: str, lang: str) -> float:
    """Get and validate float input from user."""
    while True:
        try:
            value = float(input(f"{prompt}: "))
            if value < 0:
                print(LANGUAGES[lang]["negative_value"])
                continue
            return value
        except ValueError:
            print(LANGUAGES[lang]["invalid_number"])

def main():
    # Set language and currency preferences
    lang = "tr"  # Change to "tr" for Turkish
    Currency.SYMBOL = "₺"  # Uncomment for Turkish Lira
    Currency.POSITION = "after"  # Uncomment for Turkish style
    
    texts = LANGUAGES[lang]
    
    print(f"\n{texts['title']}")
    print("-" * 30)
    
    print(f"\n{texts['enter_dates']}")
    first_day = get_date_input(texts['start_date'], lang)
    last_day = get_date_input(texts['end_date'], lang)

    print(f"\n{texts['enter_readings']}")
    first_index = get_float_input(texts['initial_reading'], lang)
    last_index = get_float_input(texts['final_reading'], lang)

    try:
        result = calculate_gas_bill(first_index, last_index, first_day, last_day, lang)
        
        print(f"\n{texts['calculation_title']}")
        print("-" * 30)
        print(f"{texts['period']}: {first_day} to {last_day}")
        print(f"{texts['consumption']}: {result['consumption_m3']:.2f} m³")
        print(f"{texts['daily_consumption']}: {result['daily_consumption_m3']:.2f} m³")
        print(f"{texts['energy_consumed']}: {result['energy_consumed_kwh']:.2f} kWh")
        print(f"{texts['daily_cost']}: {format_currency(result['daily_cost'], lang)}")
        print(f"{texts['projected_monthly']}: {format_currency(result['projected_monthly_cost'], lang)}")
        print(f"{texts['total_cost']}: {format_currency(result['total_cost_for_period'], lang)}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()





