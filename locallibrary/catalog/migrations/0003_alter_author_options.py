# Generated by Django 4.2.17 on 2024-12-24 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name']},
        ),
    ]
