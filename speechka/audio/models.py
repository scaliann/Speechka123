from django.db import models
from account.models import User

class Word(models.Model):
    word = models.CharField(max_length=255)
    def __str__(self):
        return self.word



class Audio(models.Model):
    audio_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    word = models.ForeignKey(Word, on_delete=models.DO_NOTHING, null=True)
    session = models.IntegerField()
    mongo_file_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.audio_name
