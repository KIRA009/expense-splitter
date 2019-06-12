from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Profile, Friend, FriendRequest
from django.contrib.auth import authenticate, login, logout


class Index(TemplateView):
	template_name = 'index.html'


class Register(View):
	@staticmethod
	def get(request):
		return render(request, 'register.html')

	@staticmethod
	def post(request):
		Profile.create(**request.POST)
		return redirect('login')


class Login(View):
	@staticmethod
	def get(request):
		return render(request, 'login.html')

	@staticmethod
	def post(request):
		data = request.POST
		user = authenticate(username=data['email'], password=data['password'])
		if user is not None:
			login(request, user)
			return redirect('home')
		return redirect('login')


class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		context['user'] = user
		context['friends'] = Friend.get_friends(user)
		print(context['friends'])
		context['rec_reqs'] = FriendRequest.sent_to(user)
		context['sent_reqs'] = FriendRequest.sent_by(user)
		context['pending_reqs'] = len(context['rec_reqs'])
		return context


class Logout(View):
	@staticmethod
	def get(request):
		logout(request)
		return redirect('login')


class SendRequest(View):
	@staticmethod
	def post(request):
		FriendRequest.create(request.user, **request.POST)
		return redirect('home')


class ActionRequest(View):
	@staticmethod
	def get(request, req_id, action):
		FriendRequest.act(req_id, action)
		return redirect('home')
