from immanuel import charts
from datetime import datetime


def get_moon_house(year: int, month: int, day: int, hour: int, minute: int,
                   second: int, latitude: float, longitude: float):
    """
    Returns the house number of the Moon for a given user.
    """
    # Create the natal chart object from immanuel package
    native = charts.Subject(
        date_time=datetime(year, month, day, hour, minute, second),
        latitude=latitude,
        longitude=longitude,
    )
    natal = charts.Natal(native)

    # Find the Moon object and extract its house number
    moon = next((obj for obj in natal.objects.values() if obj.name == "Moon"), None)
    if moon:
        house = moon.house
        if isinstance(house, str):
            try:
                house_number = int(house.split()[0])  # Extract the first number before "house"
                return house_number
            except ValueError:
                print(f"Error processing house for Moon: {house}")
                return None
        elif hasattr(house, 'number'):  # Assuming house has a 'number' attribute
            return house.number
        else:
            print(f"Unable to process house for Moon: {house}")
            return None
    else:
        print("Moon data not found in natal chart.")
        return None


if __name__ == "__main__":
    print("Enter details for the boy:")
    year_boy = int(input("Year: "))
    month_boy = int(input("Month: "))
    day_boy = int(input("Day: "))
    hour_boy = int(input("Hour (24-hour format): "))
    minute_boy = int(input("Minute: "))
    second_boy = int(input("Second: "))
    latitude_boy = float(input("Latitude: "))
    longitude_boy = float(input("Longitude: "))

    print("\nEnter details for the girl:")
    year_girl = int(input("Year: "))
    month_girl = int(input("Month: "))
    day_girl = int(input("Day: "))
    hour_girl = int(input("Hour (24-hour format): "))
    minute_girl = int(input("Minute: "))
    second_girl = int(input("Second: "))
    latitude_girl = float(input("Latitude: "))
    longitude_girl = float(input("Longitude: "))

    # Calculate Moon house number for the boy
    boy_moon_house = get_moon_house(
        year=year_boy,
        month=month_boy,
        day=day_boy,
        hour=hour_boy,
        minute=minute_boy,
        second=second_boy,
        latitude=latitude_boy,
        longitude=longitude_boy
    )

    # Calculate Moon house number for the girl
    girl_moon_house = get_moon_house(
        year=year_girl,
        month=month_girl,
        day=day_girl,
        hour=hour_girl,
        minute=minute_girl,
        second=second_girl,
        latitude=latitude_girl,
        longitude=longitude_girl
    )

    # Display the results
    print("\nResults:")
    print(f"Boy's Moon is in house number: {boy_moon_house}")
    print(f"Girl's Moon is in house number: {girl_moon_house}")
