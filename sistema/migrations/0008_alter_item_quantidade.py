# Generated by Django 5.0.6 on 2024-06-22 00:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sistema", "0007_alter_item_quantidade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="quantidade",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
