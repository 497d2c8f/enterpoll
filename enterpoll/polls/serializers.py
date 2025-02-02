from rest_framework import serializers
from .models import Poll


#class MainPageSerializer(serializers.Serializer):
#	most_popular_polls = serializers.ListField(child=)

class PollsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Poll
		fields = '__all__'

#class MainPageSerializer(serializers.Serializer):
#	most_popular_polls = serializers.IntegerField()

#def encode():
#	ser = MainPageSerializer(3)
