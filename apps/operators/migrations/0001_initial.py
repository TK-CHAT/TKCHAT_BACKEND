# Generated by Django 4.2 on 2023-05-05 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0004_alter_company_user'),
        ('users', '0002_user_first_name_user_last_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='operators', to=settings.AUTH_USER_MODEL)),
                ('work_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='companies.company')),
            ],
            options={
                'abstract': False,
            },
            bases=('users.user',),
        ),
    ]
