# Generated by Django 4.2 on 2023-05-06 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operator',
            name='user',
        ),
    ]
