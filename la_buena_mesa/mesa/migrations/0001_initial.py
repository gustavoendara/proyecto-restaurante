# Generated by Django 5.1.3 on 2024-11-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad', models.IntegerField()),
                ('ubicacion', models.CharField(max_length=100)),
            ],
        ),
    ]
