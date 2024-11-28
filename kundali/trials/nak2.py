from astropy.coordinates import get_body, EarthLocation
from astropy.time import Time
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import numpy as np

def calc_nakshatra(location, time, time_format="%Y-%m-%d %H:%M:%S"):
    """
    Calculates nakshatra number at input time.

    Inputs :
    location = address of your location (e.g., "Mumbai, India")
    time = time at which to calculate nakshatra
    time_format = format of input time

    Output :
    Nakshatra number at the input time (1 to 27)
    """
    # List of Nakshatra names
    nakshatram_names = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", 
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", 
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", 
        "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", 
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]
    
    nakshatram_extent = 360 / 27  # degrees
    start_coord = 23 + 47 / 60 + 14.1 / 3600  # Reference coordinate
    nakshatram_coords = np.linspace(start_coord, start_coord + nakshatram_extent * 26, 27)
    
    # Time processing
    observing_location = EarthLocation.of_address(location)
    tz_obj = TimezoneFinder()
    timezone_location = tz_obj.timezone_at(lng=observing_location.lon.value, lat=observing_location.lat.value)
    
    fmt = time_format
    date_str = time
    tz = pytz.timezone(timezone_location)
    test_date = datetime.strptime(date_str, fmt)
    local_time = tz.localize(test_date, is_dst=None)
    test_date_utc = local_time.astimezone(pytz.utc)
    test_date_utc_time = Time(test_date_utc.strftime(fmt), format="iso", scale="utc")
    
    # Get moon position
    moon_coord = get_body("moon", test_date_utc_time)
    moon_lambda = moon_coord.geocentrictrueecliptic.lon.value
    
    final_nakshatram_number = -1  # To store Nakshatra number (1 to 27)
    
    # Check Nakshatra based on moon's position
    for coord_id, coord in enumerate(nakshatram_coords):
        if coord <= moon_lambda < coord + nakshatram_extent:
            final_nakshatram_number = coord_id + 1  # Nakshatra number (1-based)
            break
    
    return final_nakshatram_number

# Example usage:
location = "Kathmandu, Nepal"
date_str = "2003-11-09 15:35:00"

nakshatra_number = calc_nakshatra(location, date_str)
print("Nakshatra number at the given time:", nakshatra_number)
