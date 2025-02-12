from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'username', 'password']
#		read_only_fields = ['pk', 'number_of_votes']

	def create(self, validated_data):
		validate_password(validated_data['password'])
		user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
		return user
