import logging

from bson import ObjectId
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import os
from pydub import AudioSegment
from django.views.generic import TemplateView
from pymongo import MongoClient

from audio.models import Audio, Word
import pymongo
import gridfs


class UploadAudioView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'message': 'User not authenticated'}, status=403)

        if 'audio' not in request.FILES or 'word' not in request.POST:
            return JsonResponse({'status': 'fail', 'message': 'No audio file or word provided'}, status=400)

        # Получаем аудиофайл и слово из запроса
        audio_file = request.FILES['audio']
        word_text = request.POST['word']

        # Ищем это слово в базе данных
        word = get_object_or_404(Word, word=word_text)
        current_session = request.session.get('audio_session', 1)
        word_id = word.id
        file_name = f'{request.user.last_name}_{current_session}_{word_id}.wav'
        # Подключаемся к MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['speechka_mdb']
        fs = gridfs.GridFS(db, collection="user_audio")
        # Сохраняем аудиофайл в MongoDB
        file_id = fs.put(audio_file.read(), filename=file_name)


        # Получаем текущую сессию из request.session




        # Создаем запись в таблице Audio с привязкой к сессии и MongoDB
        audio_record = Audio.objects.create(
            user=request.user,
            audio_name=file_name,
            word=word,
            session=current_session,
            mongo_file_id=str(file_id)  # Сохраняем ссылку на файл в MongoDB
        )

        return JsonResponse({'status': 'success', 'file_name': audio_file.name, 'mongo_file_id': str(file_id)})
class RecordingView(TemplateView):
    template_name = 'recording.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['words'] = list(Word.objects.values_list('word', flat=True))  # Преобразуем QuerySet в список
        return context

    def get(self, request, *args, **kwargs):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправляем неавторизованных пользователей

        # Находим последнюю сессию для этого пользователя
        last_session = Audio.objects.filter(user=request.user).order_by('-session').first()

        # Если сессий нет, начинаем с 1, иначе увеличиваем на 1
        if last_session:
            new_session = last_session.session + 1
        else:
            new_session = 1

        # Сохраняем новую сессию в session storage
        request.session['audio_session'] = new_session

        # Передаем номер новой сессии в контекст для рендеринга страницы
        context = self.get_context_data(**kwargs)
        context['session'] = new_session

        # Возвращаем отрендеренную страницу с новым номером сессии
        return self.render_to_response(context)


class PlayAudioView(View):
    def get(self, request, mongo_file_id):
        logging.info(f"Запрос аудиофайла с ID: {mongo_file_id}")
        try:
            # Подключаемся к MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['speechka_mdb']
            fs = gridfs.GridFS(db, collection="user_audio")

            # Получаем файл по его ID из MongoDB
            file_data = fs.get(ObjectId(mongo_file_id))
            logging.info(f"Файл найден: {file_data.filename}")

            # Возвращаем файл как HTTP-ответ
            response = HttpResponse(file_data.read(), content_type='audio/wav')
            response['Content-Disposition'] = f'inline; filename={file_data.filename}'
            return response
        except gridfs.errors.NoFile:
            logging.error(f"Файл с ID {mongo_file_id} не найден в MongoDB.")
            return HttpResponse(status=404)
        except Exception as e:
            logging.error(f"Ошибка при получении файла: {str(e)}")
            return HttpResponse(status=500)





