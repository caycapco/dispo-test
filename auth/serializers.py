from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
	User = get_user_model()
	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=User.objects.all())]
		)
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

	class Meta:
		User = get_user_model()
		model = User
		fields = ('email', 'password', 'fullname')

	def create(self, validated_data):
		User = get_user_model()
		user = User.objects.create(
			email=validated_data['email'],
			password = make_password(validated_data['password']),
			fullname=validated_data['fullname']
			)

		user.save()
		return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        #token = super().get_token(user)
    
        return token

