# Generated by Django 5.1.4 on 2025-01-07 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CSVData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=255)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("data", models.JSONField()),
            ],
        ),
    ]
