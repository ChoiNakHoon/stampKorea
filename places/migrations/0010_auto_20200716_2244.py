# Generated by Django 2.2.5 on 2020-07-16 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_auto_20200716_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='eventenddate',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='eventstartdate',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]