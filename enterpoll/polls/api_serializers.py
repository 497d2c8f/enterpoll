from drf_compound_fields.fields import ListField
from rest_framework import serializers
from .models import Poll, Choice, Comment
from rest_framework.parsers import JSONParser
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
	choices = ChoiceSerializer(many=True)

	class PollAndChoices:
		def __init__(self, poll, choices):
			self.poll = poll
			self.choices = choices

	def create(self, validated_data):

		poll_serializer = type(self.fields['poll'])(data={**validated_data['poll']})
		poll_serializer.is_valid(raise_exception=True)
		poll = poll_serializer.save(user=self.context['request'].user)

		choices_serializer = type(self.fields['choices'].child)(many=True, data=validated_data['choices'])
		choices_serializer.is_valid(raise_exception=True)
		choices = choices_serializer.save(poll=poll)

		return self.PollAndChoices(poll, choices)

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
