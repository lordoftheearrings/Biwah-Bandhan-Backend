from .models import UserDatabase
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from immanuel import charts
from datetime import datetime
from kundali.template import lagna_kundali_defn as chart
from django.core.cache import cache
from django.utils.html import escape
import os
from django.conf import settings


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


def generate_kundali_svg(year, month, day, hour, minute, second, latitude, longitude, username):
    """
    Generates the Kundali SVG for a user and saves it to the server.
    """
    # Get the Ascendant and planets with their house numbers
    ascendant, planets_in_houses = get_planets_and_houses_with_asc(
        year, month, day, hour, minute, second, latitude, longitude
    )

    # Create the LagnaChart object with the correct chartname and personname
    mychart = chart.LagnaChart("Lagna", "User", IsFullChart= True)  # Replace "User" with the actual person's name

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
    output_dir = os.path.join(settings.MEDIA_ROOT, 'kundali_svgs')
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{username}_kundali_"
    base_file_path = os.path.join(output_dir, file_name)
    

    # Generate the Kundali SVG
    mychart.draw(output_dir, file_name)  # This will create both `file_name` and `file_name.svg`

    base_file_path_without_ext = os.path.join(output_dir, file_name)  # Base file path
    if os.path.exists(base_file_path_without_ext):
        os.remove(base_file_path_without_ext)
    # Add .svg extension to the base file path
    svg_file_path = f"{base_file_path}.svg"

    # Verify the `.svg` file exists
    if not os.path.exists(svg_file_path):
        raise FileNotFoundError(f"Kundali SVG file not found: {svg_file_path}")

    # Return the `.svg` file path
    return svg_file_path

class GenerateKundaliView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        username = request.data.get("username")
        year = int(request.data.get("year"))
        month = int(request.data.get("month"))
        day = int(request.data.get("day"))
        hour = int(request.data.get("hour"))
        minute = int(request.data.get("minute"))
        second = int(request.data.get("second"))
        latitude = float(request.data.get("latitude"))
        longitude = float(request.data.get("longitude"))
        birth_location = request.data.get("birth_location")

        # Validate the user
        user = UserDatabase.objects.filter(username=username).first()
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate the Kundali SVG
        kundali_svg_file_path = generate_kundali_svg(
            year, month, day, hour, minute, second, latitude, longitude, username
        )

        # Update user data and save
        user.birth_year = year
        user.birth_month = month
        user.birth_date = day
        user.birth_hour = hour
        user.birth_minute = minute
        user.birth_second = second
        user.birth_location = birth_location
        user.birth_latitude = latitude
        user.birth_longitude = longitude
        user.kundali_svg = kundali_svg_file_path
        user.save()
        

        cache.clear()

        
        
        return Response({
            "Kundali Saved"  # Pass the SVG content to the frontend
        }, status=status.HTTP_200_OK)
    


class RetrieveKundali(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        username = request.data.get("username")
        
        # Fetch user from the database using the username
        user = UserDatabase.objects.filter(username=username).first()
        
        if not user:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Retrieve the kundali SVG file field
        kundali_svg = user.kundali_svg
        
        # Ensure the field is not empty
        if not kundali_svg:
            return Response({"message": "Kundali SVG not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Get the local file path from the FieldFile object
            file_path = kundali_svg.path # This gets the local file system path to the file
            
            # Open and read the SVG file from the file system path
            with open(file_path, 'r',encoding='utf-16') as svg_file:
                svg_content = svg_file.read()

            # Remove BOM characters (if any)
            svg_content = svg_content.lstrip('ÿþ')
            
            # Return the SVG content as a response
            return Response({
                svg_content}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle errors (e.g., file not found, read error)
            return Response({"message": f"Error reading SVG: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
