# Generated by Django 5.1.3 on 2024-11-07 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('year', models.IntegerField()),
            ],
        ),
    ]