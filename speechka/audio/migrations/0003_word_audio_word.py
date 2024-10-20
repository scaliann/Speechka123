# Generated by Django 5.1 on 2024-09-27 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0002_rename_audiomodel_audio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='audio',
            name='word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='audio.word'),
        ),
    ]
