# Generated by Django 5.0.6 on 2024-06-23 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0015_alter_geral_valor_total_atas_ganhas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geral',
            name='valor_total_atas_ganhas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
