# Generated by Django 4.1 on 2023-11-09 03:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0008_curso_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="curso",
            name="url_playlist",
            field=models.CharField(default="", max_length=255),
        ),
    ]