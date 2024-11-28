from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GunaMilanSerializer
from kundali.Guna_Milan.NakshatraBG import calc_nakshatra
from kundali.Guna_Milan.MoonBG import get_moon_house
from kundali.Guna_Milan.ashtakoot import get_guna_milan_points

class AshtakootGunMilan(APIView):
    def post(self, request):
        # Validate input data using the serializer
        serializer = GunaMilanSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # Extract boy and girl data
            boy_data = {
                "moonsign": get_moon_house(
                    year=data['year_boy'],
                    month=data['month_boy'],
                    day=data['day_boy'],
                    hour=data['hour_boy'],
                    minute=data['minute_boy'],
                    second=data['second_boy'],
                    latitude=data['latitude_boy'],
                    longitude=data['longitude_boy']
                ),
                "nakshatra": calc_nakshatra(
                    data['latitude_boy'], data['longitude_boy'], 
                    f"{data['year_boy']}-{data['month_boy']:02d}-{data['day_boy']:02d} "
                    f"{data['hour_boy']:02d}:{data['minute_boy']:02d}:{data['second_boy']:02d}"
                )
            }
            girl_data = {
                "moonsign": get_moon_house(
                    year=data['year_girl'],
                    month=data['month_girl'],
                    day=data['day_girl'],
                    hour=data['hour_girl'],
                    minute=data['minute_girl'],
                    second=data['second_girl'],
                    latitude=data['latitude_girl'],
                    longitude=data['longitude_girl']
                ),
                "nakshatra": calc_nakshatra(
                    data['latitude_girl'], data['longitude_girl'], 
                    f"{data['year_girl']}-{data['month_girl']:02d}-{data['day_girl']:02d} "
                    f"{data['hour_girl']:02d}:{data['minute_girl']:02d}:{data['second_girl']:02d}"
                )
            }

            # Calculate Guna Milan points
            guna_milan_points = get_guna_milan_points(girl_data, boy_data)
            
            return Response(guna_milan_points, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
