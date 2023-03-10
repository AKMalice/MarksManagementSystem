# Generated by Django 3.2.17 on 2023-03-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20230309_1831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_username', models.CharField(max_length=50)),
                ('teacher_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
    ]
