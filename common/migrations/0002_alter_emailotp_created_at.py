# Generated by Django 5.2.4 on 2025-07-13 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailotp',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
