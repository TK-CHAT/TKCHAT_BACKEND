# Generated by Django 4.2 on 2023-06-19 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tkbot', '0002_botprompts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botprompts',
            old_name='prompts',
            new_name='prompt',
        ),
    ]