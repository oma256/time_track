# Generated by Django 2.2 on 2020-11-04 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_payment_pg_payment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='pg_payment_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='pg_currency',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pg_description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pg_ps_amount',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Сумма оплаты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pg_user_contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Указанная почта в PayBox'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pg_user_phone',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Указанный номер тел. в PayBox'),
        ),
    ]
