from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from user_auth.forms import CustomUserAuthForm, CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = "user_auth/login.html"
    form_class = CustomUserAuthForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = "login"

class RegisterView(CreateView):
    template_name = "user_auth/register.html"
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy("task_list"))
