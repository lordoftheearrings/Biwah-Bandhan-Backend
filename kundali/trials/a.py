
from datetime import datetime
from kundali import get_vedic_chart_data

def parse_datetime(date_str):
    """Parses a date string in the format 'YYYY-MM-DD HH:MM:SS'."""
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return dt.year, dt.month, dt.day, dt.hour, dt.minute




# Gather inputs for the boy and girl
print("Enter details for the boy:")
boy_location = input("Enter location (e.g., Kathmandu, Nepal): ").strip()
boy_date = input("Enter date and time of birth (YYYY-MM-DD HH:MM:SS): ").strip()

print("\nEnter details for the girl:")
girl_location = input("Enter location (e.g., Kathmandu, Nepal): ").strip()
girl_date = input("Enter date and time of birth (YYYY-MM-DD HH:MM:SS): ").strip()

# Process boy's inputs
boy_year, boy_month, boy_day, boy_hour, boy_minute = parse_datetime(boy_date)
boy_lat, boy_lon, boy_tz = get_location_data(boy_location)

# Process girl's inputs
girl_year, girl_month, girl_day, girl_hour, girl_minute = parse_datetime(girl_date)
girl_lat, girl_lon, girl_tz = get_location_data(girl_location)

# Get the Vedic chart data for the boy
boy_data = get_vedic_chart_data(
    year=boy_year, month=boy_month, day=boy_day,
    hour=boy_hour, minute=boy_minute,
    latitude=boy_lat, longitude=boy_lon, timezone=boy_tz
)

# Get the Vedic chart data for the girl
girl_data = get_vedic_chart_data(
    year=girl_year, month=girl_month, day=girl_day,
    hour=girl_hour, minute=girl_minute,
    latitude=girl_lat, longitude=girl_lon, timezone=girl_tz
)

# Output the results
print("\nBoy's Vedic Chart Data:")
print("Ascendant:", boy_data[0])
print("Planets in Houses:", boy_data[1])

print("\nGirl's Vedic Chart Data:")
print("Ascendant:", girl_data[0])
print("Planets in Houses:", girl_data[1])
