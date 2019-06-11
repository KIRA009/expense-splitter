from django.urls import path
from .views import Index, Register, Login

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('register/', Register.as_view(), name='register'),
	path('login/', Login.as_view(), name='login')
]
