from drf_compound_fields.fields import ListField
from rest_framework import serializers
from .models import Poll, Choice, Vote, Comment
from rest_framework.parsers import JSONParser
import io
import custom_validators




class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = ['pk', 'text']
		read_only_fields = ['pk']

class PollSerializer(serializers.ModelSerializer):
	choice_set = ChoiceSerializer(many=True, min_length=2, max_length=10)

	class Meta:
		model = Poll
		fields = ['pk', 'title', 'description', 'choice_set', 'user', 'created']
		read_only_fields = ['pk', 'user', 'created']

	def create(self, validated_data):
		poll = Poll.objects.create(
			title=validated_data['title'],
			description=validated_data['description'],
			user=self.context['request'].user
		)
		choices = [Choice(poll=poll, text=choice['text']) for choice in validated_data['choice_set']]
		Choice.objects.bulk_create(choices)
		return poll




class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = ['pk', 'user', 'poll', 'choice', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		user = self.context['request'].user
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		choice = validated_data['choice']
		try:
			vote = Vote.objects.get(user=user, poll=poll)
			vote.choice = choice
			vote.save()
		except:
			vote = poll.vote_set.create(user=user, choice=choice)
		return vote




class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['pk', 'user', 'poll', 'text', 'created']
		read_only_fields = ['pk', 'user', 'poll', 'created']

	def create(self, validated_data):
		poll = Poll.objects.get(pk=self.context['request'].parser_context['kwargs']['poll_pk'])
		comment = poll.comment_set.create(user=self.context['request'].user, text=validated_data['text'])
		return comment
