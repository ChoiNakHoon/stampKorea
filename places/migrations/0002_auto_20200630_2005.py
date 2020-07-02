# Generated by Django 2.2.5 on 2020-06-30 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='place',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='places', to='places.Region'),
        ),
        migrations.AddField(
            model_name='place',
            name='region_sub',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='places', to='places.Sub_Region'),
        ),
        migrations.AddField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.Place'),
        ),
    ]
