from django.db import models
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(unique=True, primary_key=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	@classmethod
	def get(cls, email):
		try:
			return User.objects.get(email=email)
		except User.DoesNotExist:
			return None


class Profile(models.Model):
	user = models.OneToOneField('User', to_field='email', on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	expense = models.FloatField(default=0)

	objects = models.Manager()

	@classmethod
	def create(cls, **kwargs):
		user = User.objects.create_user(email=kwargs['email'][0], password=kwargs['password'][0])
		try:
			cls.objects.create(user=user, name=kwargs['name'][0])
		except IntegrityError:
			pass


class Friend(models.Model):
	user1 = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='user1')
	user2 = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='user2')
	owe = models.FloatField(default=0)  # <0 implies user1 owes user2

	objects = models.Manager()

	@classmethod
	def create(cls, user1, user2):
		cls.objects.create(user1=user1, user2=user2)

	@staticmethod
	def get_friends(user):
		friends = list()
		for friend in Friend.objects.filter(user1=user):
			friends.append(friend)
		for friend in Friend.objects.filter(user2=user):
			friends.append(friend)
		return friends

	@staticmethod
	def update(activities):
		for activity in activities:
			if not activity.settled:
				if activity.loanee is None:
					continue
				friendship = Friend.objects.get(Q(user1=activity.payer, user2=activity.loanee) |
				                                Q(user1=activity.loanee, user2=activity.payer))
				if not friendship:
					continue

				if friendship.user1 == activity.payer:
					friendship.owe += activity.money
				else:
					friendship.owe -= activity.money
				friendship.save()


class FriendRequest(models.Model):
	from_user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='from_user')
	to_user = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='to_user')
	accepted = models.BooleanField(default=False)

	objects = models.Manager()

	@classmethod
	def create(cls, user, **kwargs):
		friend = User.get(kwargs['email'][0])
		if friend is None:
			return
		if user == friend:
			return
		if len(FriendRequest.objects.filter(
				Q(from_user=user, to_user=friend) | Q(to_user=user, from_user=friend))) == 0:
			FriendRequest.objects.create(from_user=user, to_user=friend)

	@staticmethod
	def sent_to(user):
		return FriendRequest.objects.filter(to_user=user, accepted=False)

	@staticmethod
	def sent_by(user):
		return FriendRequest.objects.filter(from_user=user, accepted=False)

	@staticmethod
	def act(req_id, action):
		friend_request = FriendRequest.objects.get(id=int(req_id))
		if action == 'add':
			Friend.create(friend_request.from_user, friend_request.to_user)
			friend_request.accepted = True
			friend_request.save()
		else:
			friend_request.delete()


class Activity(models.Model):
	payer = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='owes')
	loanee = models.ForeignKey('User', on_delete=models.CASCADE, to_field='email', related_name='owe_to', null=True)
	desc = models.TextField()
	money = models.FloatField()
	settled = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	objects = models.Manager()

	@staticmethod
	def create(**kwargs):
		users = [(User.get(email), float(money)) for email, money in eval(kwargs['emails'][0]).items()]
		desc = kwargs['desc'][0]
		activities = list()
		if len(users) == 1:
			activities.append(Activity.objects.create(payer=users[0][0], loanee=None, desc=desc, money=users[0][1]))
		else:
			if not kwargs.get('payback'):
				payback = False
			else:
				payback = True
			for user in users[1:]:
				activities.append(Activity.objects.create(payer=users[0][0], loanee=user[0], desc=desc, money=user[1]))
		user = users[0][0].profile
		user.expense -= float(kwargs['expense'][0])
		user.save()
		return activities

	@staticmethod
	def get_activities(user):
		return Activity.objects.filter(Q(payer=user) | Q(loanee=user)).filter(~Q(loanee=None)).order_by('-date')

	@staticmethod
	def get_expenses(user):
		return Activity.objects.filter(payer=user, loanee=None)

	@staticmethod
	def delete_exp(user, act_id):
		activity = Activity.objects.get(id=int(act_id), payer=user, loanee=None)
		if activity:
			user = activity.payer.profile
			user.expense += activity.money
			user.save()
			activity.delete()

	@staticmethod
	def delete_act(user, act_id):
		activity = Activity.objects.get(loanee=user, id=act_id)
		if activity:
			payer = activity.payer
			loanee = activity.loanee
			payer.profile.expense += activity.money
			payer.profile.save()
			loanee.profile.expense -= activity.money
			loanee.profile.save()
			friendship = Friend.objects.filter(Q(user1=payer, user2=loanee) | Q(user2=payer, user1=loanee))[0]
			if friendship.user1 == loanee:
				friendship.owe += activity.money
			else:
				friendship.owe -= activity.money
			friendship.save()
			activity.settled = True
			activity.save()
