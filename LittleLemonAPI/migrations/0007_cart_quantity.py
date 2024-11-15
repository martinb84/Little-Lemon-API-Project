# Generated by Django 4.2 on 2024-04-09 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0006_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
