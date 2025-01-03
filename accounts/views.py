from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from utils import send_otp_code
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from .models import OtpCode, User
import random

class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'We sent you a code verification', 'success')
            return redirect('accounts:verify-code')
        return render(request, self.template_name, {'form':form})

class UserRegisterVerifyCodeView(View) :
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                         user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'You registered successfully', 'success')
                return redirect('accounts:verify-code')
            else:
                messages.error(request, 'This code is wrong.', 'danger')
            return redirect('home:home')

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You lagged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Phone or password is wrong.', 'danger')
        return render(request, self.template_name, {'form':form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully', 'success')
        return redirect('home:home')