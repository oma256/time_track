# Generated by Django 2.2 on 2020-10-22 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20201022_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Пакет по умолчанию'),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='month_price',
            field=models.DecimalField(decimal_places=1, max_digits=10, verbose_name='Цена за 1 месяц'),
        ),
    ]
