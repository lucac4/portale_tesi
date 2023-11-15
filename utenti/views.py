from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

class UserLoginView(LoginView):
    template_name = 'login.html'
    form = AuthenticationForm

class UserLogoutView(LogoutView):
    pass

# Create your views here.
def registration(request):
    form = UserCreationForm
    context = {'form': form}
    return render(request, 'registration.html', context)