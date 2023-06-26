# Generated by Django 4.2 on 2023-06-26 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('work_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='companies.company')),
            ],
            options={
                'abstract': False,
            },
            bases=('users.user',),
        ),
    ]
