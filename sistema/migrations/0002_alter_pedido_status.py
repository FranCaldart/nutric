# Generated by Django 5.0.6 on 2024-07-10 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sistema", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("e", "Em entrega"),
                    ("f", "Finalizado"),
                    ("n", "Não iniciado"),
                ],
                max_length=1,
                null=True,
            ),
        ),
    ]
