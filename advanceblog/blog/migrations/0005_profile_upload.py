# Generated by Django 5.0.1 on 2024-01-09 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_profile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='upload',
            field=models.ImageField(default='static/default_profile_pic.jpg', upload_to='profilepics/'),
        ),
    ]
