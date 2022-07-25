from rest_framework import serializers
from .models import Facility

class FacilitySerializer(serializers.ModelSerializer):
	name = serializers.CharField(max_length=32)
	latitude = serializers.DecimalField(decimal_places=14,max_digits=17)
	longitude = serializers.DecimalField(decimal_places=14,max_digits=17)

	class Meta:
		model = Facility
		fields= ('__all__')