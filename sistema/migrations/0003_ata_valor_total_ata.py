# Generated by Django 5.0.6 on 2024-06-19 22:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sistema", "0002_alter_item_quantidade_restante_resumo"),
    ]

    operations = [
        migrations.AddField(
            model_name="ata",
            name="valor_total_ata",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=200, null=True
            ),
        ),
    ]
