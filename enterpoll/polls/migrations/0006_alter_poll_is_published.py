# Generated by Django 5.1.4 on 2025-02-03 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_poll_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
