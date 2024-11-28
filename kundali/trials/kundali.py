from vedicastro import VedicAstro
from datetime import datetime
from flatlib import const
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
import template.lagna_kundali_defn as chart

def get_vedic_chart_data(year: int, month: int, day: int, hour: int, minute: int,
                         latitude: float, longitude: float, timezone: str = None):
    """
    Returns basic Vedic chart information including ascendant and planets in houses.

    Parameters:
    -----------
    year, month, day: Date components
    hour, minute: Time components (24-hour format)
    latitude, longitude: Location coordinates
    timezone: Optional timezone string (e.g., 'America/New_York')
    """

    # Create VedicHoroscopeData instance
    chart_data = VedicAstro.VedicHoroscopeData(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=0,
        latitude=latitude,
        longitude=longitude,
        tz=timezone
    )

    # Generate the chart
    chart = chart_data.generate_chart()

    # Get planets and houses data
    planets_data = chart_data.get_planets_data_from_chart(chart)

    # Get Ascendant information
    asc_data = next(p for p in planets_data if p.Object == 'Asc')
    ascendant = asc_data.Rasi

    # Get Planets in Houses
    planets_in_houses = {}
    for planet in planets_data:
        if planet.Object != 'Asc' and planet.Object not in ["Uranus","Neptune","Pluto","Chiron", "Syzygy", "Fortuna"]:
            planets_in_houses[planet.Object] = planet.HouseNr

    return ascendant, planets_in_houses

# Example usage with user input
if __name__ == "__main__":
    # Prompt the user for input
    year = int(input("Enter the year: "))
    month = int(input("Enter the month: "))
    day = int(input("Enter the day: "))
    hour = int(input("Enter the hour (24-hour format): "))
    minute = int(input("Enter the minute: "))
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))
    timezone = input("Enter the timezone (e.g., 'America/New_York'): ")

    # Get the Vedic chart data
    ascendant, planets_in_houses = get_vedic_chart_data(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone
    )

    # Create the LagnaChart object
    mychart = chart.LagnaChart("Lagna", "Sample", IsFullChart=True)

    # Set the ascendant sign
    mychart.set_ascendantsign(ascendant)

    # Define planet colors
    planet_colors = {
        "Sun": 'darkred',
        "Moon": 'black',
        "Mars": 'black',
        "Mercury": 'black',
        "Jupiter": 'black',
        "Venus": 'black',
        "Saturn": 'black',
        "Rahu": 'black',
        "Ketu": 'black'
    }

    # Add the planets to the chart with colors
    planet_mapping = {
        "Sun": chart.SUN,
        "Moon": chart.MOON,
        "Mars": chart.MARS,
        "Mercury": chart.MERCURY,
        "Jupiter": chart.JUPITER,
        "Venus": chart.VENUS,
        "Saturn": chart.SATURN,
        "Rahu": chart.RAHU,
        "Ketu": chart.KETU
    }

    for planet, house in planets_in_houses.items():
        mychart.add_planet(planet_mapping[planet], planet[:2], house, colour=planet_colors[planet])

    # Update chart configuration
    mychart.updatechartcfg(aspect=False, clr_outbox='maroon', clr_background='yellow', clr_line='brown', clr_houses=['khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown'])

    # Draw the chart
    if mychart.draw("C:\\Users\\Hp\\Documents\\Kundali\\Kundali Output", "Birth Chart Sample"):
        print("SUCCESS")
