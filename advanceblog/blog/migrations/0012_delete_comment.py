# Generated by Django 4.2.5 on 2024-01-15 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_tags_embedding'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
