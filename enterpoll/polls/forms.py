from django import forms
from polls.models import Poll, Choice, Comment

class PollModelForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['title', 'description']
		widgets = {
			'title': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
			'description': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
		}

class CommentModelForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']
		widgets = {
			'text': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'required': True})
		}
		labels = {
			'text': ''
		}
