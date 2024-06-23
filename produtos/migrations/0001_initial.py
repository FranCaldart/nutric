# Generated by Django 5.0.6 on 2024-06-19 01:26

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Produto",
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
                ("produto", models.CharField(max_length=20)),
                ("descricao", models.CharField(max_length=200)),
            ],
        ),
    ]
