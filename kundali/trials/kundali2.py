from immanuel import charts
from datetime import datetime
import template.lagna_kundali_defn as chart
from vedicastro import VedicAstro


def get_planets_and_houses(year: int, month: int, day: int, hour: int, minute: int,
                           second: int, latitude: float, longitude: float):
    """
    Returns the planets and their corresponding house numbers.
    """
    # Create the natal chart object from immanuel package
    native = charts.Subject(
        date_time=datetime(year, month, day, hour, minute, second),
        latitude=latitude,
        longitude=longitude,
    )
    natal = charts.Natal(native)

    # Specify the desired planets and nodes
    desired_objects = [
        "Asc", "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "True North Node", "True South Node"
    ]

    planets_in_houses = {}
    
    # Collect the house number for each planet
    for obj in natal.objects.values():
        if obj.name in desired_objects:
            house = obj.house
            planet = obj.name
            if planet == "True North Node":
                planet = "Rahu"
            elif planet == "True South Node":
                planet = "Ketu"
            
            # Print the type and value of house for debugging
            print(f"Planet: {planet}, House: {house}, Type of House: {type(house)}")

            # Check if house is a string or object, and process accordingly
            if isinstance(house, str):
                try:
                    house_number = int(house.split()[0])  # Extract the first number before "house"
                    planets_in_houses[planet] = house_number
                except ValueError:
                    print(f"Error processing house for {planet}: {house}")
            elif hasattr(house, 'number'):  # Assuming house has a 'number' attribute
                house_number = house.number
                planets_in_houses[planet] = house_number
            else:
                print(f"Unable to process house for {planet}: {house}")

    return planets_in_houses


def get_vedic_chart_data(year: int, month: int, day: int, hour: int, minute: int,
                         latitude: float, longitude: float, timezone: str = None):
    """
    Returns basic Vedic chart information including ascendant and planets in houses.
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
    ascendant = asc_data.Rasi  # Ascendant sign (Rasi)

    return ascendant


# Main function to get and map planets and houses
if __name__ == "__main__":
    # Prompt the user for input
    year = int(input("Enter the year: "))
    month = int(input("Enter the month: "))
    day = int(input("Enter the day: "))
    hour = int(input("Enter the hour (24-hour format): "))
    minute = int(input("Enter the minute: "))
    second = int(input("Enter the second: "))
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))
    timezone = input("Enter the timezone (e.g., 'Asia/Kathmandu'): ")

    # Get the Vedic chart data for Ascendant
    ascendant = get_vedic_chart_data(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone
    )

    # Get the planets and their house numbers from Immanuel
    planets_in_houses = get_planets_and_houses(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        latitude=latitude,
        longitude=longitude
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

    # Planet mappings
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

    # Add the planets to the chart with colors
    for planet, house in planets_in_houses.items():
        if planet in planet_mapping:  # Ensure the planet exists in the chart mapping
            mychart.add_planet(planet_mapping[planet], planet[:2], house, colour=planet_colors[planet])

    # Update chart configuration
    mychart.updatechartcfg(aspect=False, clr_outbox='maroon', clr_background='yellow', clr_line='brown', clr_houses=['khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown'])

    # Draw the chart
    if mychart.draw("C:\\Users\\Hp\\Documents\\Kundali\\Kundali Output", "Birth Chart Sample"):
        print("SUCCESS")
