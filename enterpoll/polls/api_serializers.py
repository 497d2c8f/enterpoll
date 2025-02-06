from drf_compound_fields.fields import ListField
from rest_framework import serializers
from .models import Poll, Choice, Comment
from rest_framework.parsers import JSONParser
from collections import namedtuple
import io
import custom_validators

class PollListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['pk', 'title', 'description', 'user', 'created']

class PollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['title', 'description']

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = ['text']

class PollAndChoicesSerializer(serializers.Serializer):
	poll = PollSerializer()
	choices = serializers.ListField(child=ChoiceSerializer(), min_length=2, max_length=10)

#	class PollAndChoices:
#		def __init__(self, poll, choices):
#			self.poll = poll
#			self.choices = choices

	poll_and_choices = namedtuple('PollAndChoices', ['poll', 'choices'])

	def create(self, validated_data):
		poll = Poll.objects.create(**validated_data['poll'], user=self.context['request'].user)
		choices = Choice.objects.bulk_create([Choice(poll=poll, text=choice['text']) for choice in validated_data['choices']])
		return self.poll_and_choices(poll, choices)

class DetailedPollSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = ['pk', 'title', 'description', 'user', 'created']

class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['pk', 'user', 'poll', 'text', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['pk', 'user', 'poll', 'text', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		comment = poll.comment_set.create(user=self.context['request'].user, text=validated_data['text'])
		return comment
