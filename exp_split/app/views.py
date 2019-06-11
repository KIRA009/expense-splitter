from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class Index(TemplateView):
	template_name = 'index.html'


class Register(View):
	@staticmethod
	def get(request):
		return render(request, 'register.html')

	@staticmethod
	def post(request):
		data = request.POST
		print(data)
		return redirect('login')


class Login(View):
	@staticmethod
	def get(request):
		return render(request, 'login.html')

	@staticmethod
	def post(request):
		data = request.POST
		print(data)
		return redirect('login')
