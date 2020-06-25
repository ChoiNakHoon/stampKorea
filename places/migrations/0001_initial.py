# Generated by Django 2.2.5 on 2020-06-23 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(choices=[('A01', 'Nature'), ('A02', 'Culture/Art/History'), ('A03', 'Leisure/Sports'), ('A04', 'Shopping'), ('A05', 'Cuisine'), ('B02', 'Accommodation')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('directions', models.TextField()),
                ('tel', models.CharField(max_length=20)),
                ('mapy', models.CharField(max_length=20)),
                ('mapx', models.CharField(max_length=20)),
                ('zipcode', models.CharField(max_length=10)),
                ('created_time', models.CharField(max_length=20)),
                ('updated_time', models.CharField(max_length=20)),
                ('info_center', models.CharField(max_length=255)),
                ('parking', models.CharField(max_length=15)),
                ('rest_date', models.CharField(max_length=30)),
                ('use_time', models.TextField()),
                ('cat_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='places', to='places.Cat_Type')),
                ('likes', models.ManyToManyField(blank=True, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sub_Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region', to='places.Region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sub_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=20)),
                ('text', models.CharField(max_length=255)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='info', to='places.Place')),
            ],
            options={
                'abstract': False,
            },
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
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(max_length=80)),
                ('file', models.ImageField(upload_to='place_photos')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.Place')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
