from rest_framework import serializers
from .models import Poll


class PollsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['pk']

class CreatePollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		exclude = ['created', 'user', 'is_published']
