from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FacilitySerializer
from .models import Facility
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models.expressions import RawSQL

class FacilityViews(APIView):
	def post(self, request):
		serializer = FacilitySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
		else:
			return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, id=None):
		if id:
			item = Facility.objects.get(id=id)
			serializer = FacilitySerializer(item)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		items = Facility.objects.locations_near_x_within_y_km(100,50,100)
		print(items)

		#locs = get_locations_nearby_coords(100,1,None)
		latitude = 12
		longitude = 1
		max_distance=None

	#def get_locations_nearby_coords(latitude, longitude, max_distance=None):
		gcd_formula = "6371 * acos(least(greatest(\
		cos(radians(%s)) * cos(radians(latitude)) \
		* cos(radians(longitude) - radians(%s)) + \
		sin(radians(%s)) * sin(radians(latitude)) \
		, -1), 1))"

		distance_raw_sql = RawSQL(gcd_formula,(latitude, longitude, latitude))
		qs = Facility.objects.all() \
		.annotate(distance=distance_raw_sql) \
		.order_by('distance')

		if max_distance is not None:
			qs = qs.filter(distance__lt=max_distance)

		#return qs
		print('locs:', qs)
		#items = Facility.objects.all()
		serializer = FacilitySerializer(qs, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
