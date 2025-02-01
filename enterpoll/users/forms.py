from django.contrib.auth.forms import UserCreationForm
import custom_validators

class UserCreationForm(UserCreationForm):

	def clean(self):
		cleaned_data = super().clean()
		custom_validators.forbidden_words(cleaned_data['username'])
		return cleaned_data
