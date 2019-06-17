from django.urls import path
from .views import Index, Register, Login, Home, SendRequest, ActionRequest, AddExpense, DeleteExpense, SettleExpense, \
	Logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('register/', Register.as_view(), name='register'),
	path('login/', Login.as_view(), name='login'),
	path('home/', login_required(Home.as_view()), name='home'),
	path('send-request/', login_required(SendRequest.as_view()), name='send_request'),
	path('action-request/<int:req_id>/<str:action>/', login_required(ActionRequest.as_view()), name='action_request'),
	path('add-expense/', login_required(AddExpense.as_view()), name='add_expense'),
	path('delete-expense/', login_required(DeleteExpense.as_view()), name='delete_expense'),
	path('settle-expense/', login_required(SettleExpense.as_view()), name='settle-expense'),
	path('logout/', login_required(Logout.as_view()), name='logout')
]
