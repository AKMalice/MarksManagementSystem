# Generated by Django 3.2.17 on 2023-07-08 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('user_type', models.CharField(max_length=50)),
                ('token', models.CharField(max_length=50)),
            ],
        ),
    ]
