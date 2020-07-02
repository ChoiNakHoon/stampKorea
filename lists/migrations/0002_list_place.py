# Generated by Django 2.2.5 on 2020-06-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='place',
            field=models.ManyToManyField(blank=True, related_name='lists', to='places.Place'),
        ),
    ]
