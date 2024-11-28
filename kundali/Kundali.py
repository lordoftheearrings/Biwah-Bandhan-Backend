from immanuel import charts
from datetime import datetime
from kundali.template import lagna_kundali_defn as chart

def get_planets_and_houses_with_asc(year: int, month: int, day: int, hour: int, minute: int,
                                    second: int, latitude: float, longitude: float):
    """
    Returns the Ascendant sign and the planets with their corresponding house numbers.
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
    ascendant = None

    # Collect the house number and Ascendant
    for obj in natal.objects.values():
        if obj.name in desired_objects:
            house = obj.house
            planet = obj.name
            if planet == "True North Node":
                planet = "Rahu"
            elif planet == "True South Node":
                planet = "Ketu"
            
            if planet == "Asc":
                ascendant = obj.sign.name  # Capture the Ascendant sign name
            else:
                # Process house number
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

    return ascendant, planets_in_houses


def generate_kundali_svg(year, month, day, hour, minute, second, latitude, longitude):
    # Get the Ascendant and planets with their house numbers
    ascendant, planets_in_houses = get_planets_and_houses_with_asc(
        year, month, day, hour, minute, second, latitude, longitude
    )

    # Create the LagnaChart object
    mychart = chart.LagnaChart("Lagna", "Sample", IsFullChart=True)

    # Set the Ascendant sign
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
    mychart.updatechartcfg(
        aspect=False,
        clr_outbox='maroon',
        clr_background='yellow',
        clr_line='brown',
        clr_houses=[
            'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown',
            'khaki', 'sandybrown', 'sandybrown', 'khaki', 'sandybrown', 'sandybrown'
        ]
    )

    # Generate the SVG as a string
    svg_string = mychart.draw_to_svg()

    return svg_string
