# Generated by Django 4.2 on 2023-06-17 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wsp', '0002_alter_messagewsp_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagewsp',
            name='role',
            field=models.CharField(choices=[('SYSTEM', 'SYSTEM'), ('SYSTEM', 'USER'), ('ASSISTANT', 'ASSISTANT')], default='SYSTEM', max_length=10),
        ),
    ]
