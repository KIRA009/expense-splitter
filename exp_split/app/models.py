from django.db import models
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

	@classmethod
	def get_friends(cls, user):
		friends = list()
		for friend in cls.objects.filter(user1=user):
			friends.append(friend)
		for friend in cls.objects.filter(user2=user):
			friends.append(friend)
		return friends


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
		if len(FriendRequest.objects.filter(models.Q(from_user=user, to_user=friend) | models.Q(to_user=user, from_user=friend))) == 0:
			FriendRequest.objects.create(from_user=user, to_user=friend)

	@classmethod
	def sent_to(cls, user):
		return cls.objects.filter(to_user=user, accepted=False)

	@classmethod
	def sent_by(cls, user):
		return cls.objects.filter(from_user=user, accepted=False)

	@classmethod
	def act(cls, req_id, action):
		friend_request = FriendRequest.objects.get(id=int(req_id))
		if action == 'add':
			Friend.create(friend_request.from_user, friend_request.to_user)
			friend_request.accepted = True
			friend_request.save()
		else:
			friend_request.delete()
