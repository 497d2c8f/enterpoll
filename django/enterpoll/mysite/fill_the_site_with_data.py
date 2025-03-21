from django.contrib.auth.models import User
from enterpoll.models import Poll, Choice, Vote, Rating, Comment
import wonderwords
import random

NUMBER_OF_POLLS = 100
NUMBER_OF_USERS = 100

print('The database is being filled in...')

User.objects.all().delete()
Poll.objects.all().delete()
Choice.objects.all().delete()
Vote.objects.all().delete()
Rating.objects.all().delete()
Comment.objects.all().delete()

TEXT = 'Suspendisse potenti. Nullam non purus a tortor interdum gravida eu at metus. Maecenas ornare imperdiet tincidunt. In vulputate mollis sapien. Maecenas at lacus massa. Sed feugiat, mauris ut finibus ullamcorper, urna ante porta est, non tempor sem magna sit amet augue. Phasellus vitae mi ac felis laoreet vulputate. Nam quis turpis non sem auctor vulputate et vel est. Aenean sed nulla eu leo bibendum semper sed vel eros. Vivamus in magna eget nulla euismod malesuada quis ut orci. Phasellus sed nibh et massa bibendum ultricies. Nunc sagittis luctus erat ut sodales. Donec et nisl hendrerit, ornare erat et, lacinia elit. Fusce eu eleifend erat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam condimentum, diam id egestas ornare, ex massa congue felis, non tempor sapien nunc sed augue. Etiam eu est vel risus pellentesque posuere. Duis molestie facilisis augue a lobortis. Sed ullamcorper, nisi et condimentum euismod, dolor elit mattis erat, ut iaculis turpis dolor at nunc. Praesent aliquet arcu ligula, vitae viverra dui pulvinar vitae. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nunc facilisis eleifend nunc, ac aliquet lorem ullamcorper semper. Maecenas pulvinar et dolor eget facilisis. Donec pellentesque consectetur justo ac sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae. In sodales, tellus eget congue pulvinar, sapien turpis interdum leo, eget facilisis eros lacus vel dui. Donec sit amet tellus non erat suscipit malesuada. Sed gravida odio non tortor scelerisque fringilla. Donec metus justo, placerat vel lobortis eu, laoreet ac justo. Integer dolor risus, fringilla eget risus at, euismod feugiat ex. Nullam non iaculis sem. Vestibulum hendrerit lacus eu quam bibendum faucibus. Nulla sit amet dui quis nisi congue tempor non et orci. Pellentesque et ex vel nulla congue suscipit. Nullam ut dignissim eros. Suspendisse sit amet pulvinar ante. Proin varius porta risus quis pretium. Nullam sed sapien magna. Aliquam nunc massa, dictum ac odio id, efficitur dapibus felis. Integer accumsan elementum sodales. Nullam leo libero, consequat in condimentum sed, convallis ac turpis. Mauris suscipit id leo a vehicula. Duis rutrum ante nec urna aliquam, vehicula rutrum velit lacinia. Etiam non consequat augue, tempus rutrum sem. Etiam bibendum dapibus velit eget malesuada. Nullam maximus rutrum molestie. Quisque at felis risus. Quisque pharetra porta justo, vel aliquam lacus hendrerit sed. Mauris mollis mauris pulvinar dictum lacinia. Phasellus quam turpis, lobortis eu rutrum sed, gravida eu dolor. '

TEXT = TEXT.replace(',', '').replace('.', '').lower()
WORDS = list(set(TEXT.split(' ')))

def get_random_word(min_length=1):
	while True:
		word = random.choice(WORDS)
		if len(word) >= min_length:
			return word
		else:
			continue

def get_random_username():
	return get_random_word(4).capitalize() + str(random.randint(1, 99))

def get_random_sentense():
	return ' '.join(random.choices(WORDS, k=random.randint(3, 8))).capitalize()

random_word = wonderwords.RandomWord()
random_sentence = wonderwords.RandomSentence()

User.objects.create_user(username='User1', password='Helloworld1')
User.objects.create_superuser(username='admin', password='admin')

users = []

for i in range(NUMBER_OF_USERS):
	users.append(User.objects.create_user(username=get_random_username(), password='Helloworld1'))

for _ in range(NUMBER_OF_POLLS):

	poll = Poll.objects.create(title=get_random_sentense() + '?', description=get_random_sentense(), user=random.choice(users))

	random_number_of_choices = random.randint(2, 10)
	choices = []
	for _ in range(random_number_of_choices):
		choices.append(Choice.objects.create(poll=poll, text=get_random_sentense()))

	random_number_of_votes = random.randint(0, NUMBER_OF_USERS)
	for _ in range(random_number_of_votes):
		random_user = random.choice(users)
		random_choice = random.choice(choices)
		Vote.objects.filter(user=random_user, poll=poll) or Vote.objects.create(user=random_user, poll=poll, choice=random_choice)

	random_number_of_ratings = random.randint(0, NUMBER_OF_USERS)
	for _ in range(random_number_of_ratings):
		random_user = random.choice(users)
		random_value = random.randint(random.randint(1, 4), 5)
		Rating.objects.filter(user=random_user, poll=poll) or Rating.objects.create(user=random_user, poll=poll, value=random_value)

	random_number_of_comments = random.randint(0, NUMBER_OF_USERS)
	for _ in range(random_number_of_comments):
		random_user = random.choice(users)
		random_comment_text = get_random_sentense()
		Comment.objects.create(user=random.choice(users), poll=poll, text=random_comment_text)

print('Filling in the database is completed.')
