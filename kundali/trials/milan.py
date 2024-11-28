from immanuel import charts
from datetime import datetime

native = charts.Subject(
        date_time=datetime(2002, 11, 9, 13, 00, 0),
        latitude=27.7,
        longitude=85.3,
    )



natal = charts.Natal(native)

for object in natal.objects.values():
    print(object)