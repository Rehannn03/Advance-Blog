# Generated by Django 5.0.1 on 2024-01-09 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_upload_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to='profilepics/'),
        ),
    ]
