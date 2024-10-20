from django.urls import path

from .views import *



urlpatterns = [
    path('upload/', UploadAudioView.as_view(), name='upload'),
    path('recording/', RecordingView.as_view(), name='recording'),
    path('play_audio/<str:mongo_file_id>/', PlayAudioView.as_view(), name='play_audio'),
]
