# Generated by Django 4.1.6 on 2023-02-13 15:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_alter_pet_group_alter_pet_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="weight",
            field=models.FloatField(),
        ),
    ]
