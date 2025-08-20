from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        # Отправка приветственного письма
        send_mail(
            'Добро пожаловать в наш магазин!',
            f'Приветствуем вас, {user.email}! Спасибо за регистрацию.',
            'admin@myshop.com',
            [user.email],
            fail_silently=False,
        )

        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return reverse_lazy('product_list')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('product_list')


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('product_list')

    def get_object(self, queryset=None):
        return self.request.user
