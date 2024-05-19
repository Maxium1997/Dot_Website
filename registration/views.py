from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import MemberCreationForm

# Create your views here.


class SignUpView(CreateView):
    form_class = MemberCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'registration/logout_done.html')
    else:
        return render(request, 'registration/logout_check.html')
