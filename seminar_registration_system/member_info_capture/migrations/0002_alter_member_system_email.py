# Generated by Django 4.2.4 on 2023-08-18 04:28

from django.db import migrations, models
import member_info_capture.models


class Migration(migrations.Migration):

    dependencies = [
        ('member_info_capture', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='system_email',
            field=models.EmailField(default=member_info_capture.models.generate_system_email, max_length=254, unique=True),
        ),
    ]
