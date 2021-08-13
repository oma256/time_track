# Generated by Django 2.2 on 2020-10-13 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VersionControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255, verbose_name='Версия приложения')),
                ('force_update', models.BooleanField(default=False, verbose_name='Принудительное обновление')),
            ],
            options={
                'verbose_name': 'Управление версией приложения',
                'verbose_name_plural': 'Управление версиями приложения',
            },
        ),
    ]