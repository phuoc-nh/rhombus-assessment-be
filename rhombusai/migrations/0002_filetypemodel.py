# Generated by Django 5.1.3 on 2024-11-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rhombusai', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=255)),
                ('type', models.JSONField()),
            ],
        ),
    ]
