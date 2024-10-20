

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, TemplateView, ListView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.viewsets import ViewSet

from audio.models import Audio
from .forms import UserLoginForm, UserRegistrationForm
from .models import User



class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context


class UserRegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()

        # Важно вернуть родительский метод form_valid для корректного завершения
        return super().form_valid(form)


class UserProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все аудиофайлы текущего пользователя
        user_audio_files = Audio.objects.filter(user=self.request.user)
        sessions = Audio.objects.filter(user=self.request.user).values_list('session', flat=True).distinct()
        context['user_audio_files'] = user_audio_files
        context['sessions'] = sessions
        return context



class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Перенаправление после выхода на главную страницу

    # Дополнительная логика при логауте (если требуется)
    def dispatch(self, request, *args, **kwargs):
        # Например, ты можешь добавить логику записи в лог или другие действия
        return super().dispatch(request, *args, **kwargs)




class SessionList(ListView):
    template_name = 'session_list.html'
    context_object_name = 'sessions'  # Как будет называться список сессий в шаблоне

    def get_queryset(self):
        # Получаем все сессии пользователя
        sessions = Audio.objects.filter(user=self.request.user).values_list('session', flat=True)

        # Убираем дубликаты сессий с помощью Python (например, через set)
        unique_sessions = list(set(sessions))
        unique_sessions.sort()  # Сортируем для порядка, если нужно

        # Возвращаем уникальные сессии для отображения в шаблоне
        return unique_sessions

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)

        # Выводим в консоль для отладки
        print("Контекст сессий:", context['sessions'])

        return context

class SessionDetail(TemplateView):
    template_name = 'session_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем значение параметра session через self.kwargs
        session = self.kwargs['session']
        # Добавляем в контекст саму сессию и аудиофайлы для этой сессии
        context['session'] = session
        context['audio_files'] = Audio.objects.filter(user=self.request.user, session=session)
        return context



