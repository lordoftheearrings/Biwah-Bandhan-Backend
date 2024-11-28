from Guna_Milan.NakshatraBG import calc_nakshatra
from Guna_Milan.MoonBG import get_moon_house
from Guna_Milan.ashtakoot import get_guna_milan_points


if __name__ =="__main__":
    print("Enter details for the boy:")
    year_boy = int(input("Year: "))
    month_boy = int(input("Month: "))
    day_boy = int(input("Day: "))
    hour_boy = int(input("Hour (24-hour format): "))
    minute_boy = int(input("Minute: "))
    second_boy = int(input("Second: "))
    latitude_boy = float(input("Latitude: "))
    longitude_boy = float(input("Longitude: "))
    #boy_location = input("Enter location (e.g., Kathmandu, Nepal): ")
    boy_date = f"{year_boy}-{month_boy:02d}-{day_boy:02d} {hour_boy:02d}:{minute_boy:02d}:{second_boy:02d}"

    print("\nEnter details for the girl:")
    year_girl = int(input("Year: "))
    month_girl = int(input("Month: "))
    day_girl = int(input("Day: "))
    hour_girl = int(input("Hour (24-hour format): "))
    minute_girl = int(input("Minute: "))
    second_girl = int(input("Second: "))
    latitude_girl = float(input("Latitude: "))
    longitude_girl = float(input("Longitude: "))
    #girl_location = input("Enter location (e.g., Kathmandu, Nepal): ")
    girl_date = f"{year_girl}-{month_girl:02d}-{day_girl:02d} {hour_girl:02d}:{minute_girl:02d}:{second_girl:02d}"
    
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

    boy_nakshatra = calc_nakshatra(latitude_boy,longitude_boy, boy_date)
    girl_nakshatra = calc_nakshatra(latitude_girl,longitude_girl, girl_date)

    boy = {"moonsign": boy_moon_house, "nakshatra": boy_nakshatra}
    girl = {"moonsign": girl_moon_house, "nakshatra": girl_nakshatra}

    guna_milan_points = get_guna_milan_points(girl,boy)

    
    print("\nResults:")

    print(f"Varna(max 1) = {guna_milan_points['varna']}")
    print(f"Vasya(max 2) = {guna_milan_points['vasya']}")
    print(f"Tara(max 3) = {guna_milan_points['tara']}")
    print(f"Yoni(max 4) = {guna_milan_points['yoni']}")
    print(f"Grah Maitri(max 5) = {guna_milan_points['grah']}")
    print(f"Gana(max 6) = {guna_milan_points['gana']}")
    print(f"Rashi/Bhakoota(max 7) = {guna_milan_points['bhakoot']}")
    print(f"Nadi(max 8) = {guna_milan_points['nadi']}")
    print(f"Total Guna Milan Points(max 36) = {guna_milan_points['total']}")
    