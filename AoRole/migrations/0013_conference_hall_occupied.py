# Generated by Django 4.0.6 on 2022-07-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AoRole', '0012_remove_conference_hall_occupied_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference_hall',
            name='occupied',
            field=models.BooleanField(default=False),
        ),
    ]