# Generated by Django 2.2 on 2020-10-22 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20201022_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена'),
        ),
    ]