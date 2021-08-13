# Generated by Django 2.2 on 2020-10-22 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('organizations', '0003_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationTariffPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tariffs', to='organizations.Organization')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizations', to='payment.Package')),
            ],
            options={
                'verbose_name': 'Тариф организации',
                'verbose_name_plural': 'Тарифы организаций',
            },
        ),
    ]
