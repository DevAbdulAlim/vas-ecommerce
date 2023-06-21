from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render,redirect
from django.views import View
from .forms import RegistrationForm, LoginForm

# Create your views here.
class ProfileView(View):
    def get(self, request):
        return render(request, 'user/profile.html')


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']

            user = User.objects.create_user(username=username, email=email, password=password1)

            profile = Profile.objects.create(user=user, phone_number=phone_number, address=address)

            login(request, user)
            return redirect('user:profile')
        else:
            # Display from validation errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            return render(request, 'user/register.html', {'form': form, 'error_messages': error_messages})



class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(data=request.POST) # Pass the 'data' parameter here
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user:profile')
        else:
            error_message = "Username and password do not match."
            return render(request, 'user/login.html', {'form': form, 'error_message': error_message,})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:home')