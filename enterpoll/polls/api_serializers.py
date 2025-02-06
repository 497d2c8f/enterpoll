from drf_compound_fields.fields import ListField
from rest_framework import serializers
from .models import Poll, Choice
from rest_framework.parsers import JSONParser
import io
import custom_validators

class PollsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['pk']

class PollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['title', 'description']

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = ['text']

class CompletePoll:
	def __init__(self, poll, choices):
		self.poll = poll
		self.choices = choices

class CompletePollSerializer(serializers.Serializer):
	poll = PollSerializer()
	choices = ChoiceSerializer(many=True)

	def create(self, validated_data):

		poll_serializer = type(self.fields['poll'])(data={**validated_data['poll']})
		poll_serializer.is_valid(raise_exception=True)
		poll = poll_serializer.save(user=self.context['request'].user)

		choices_serializer = type(self.fields['choices'].child)(many=True, data=validated_data['choices'])
		choices_serializer.is_valid(raise_exception=True)
		choices = choices_serializer.save(poll=poll)

		return CompletePoll(poll, choices)
