# Generated by Django 4.1.5 on 2023-05-18 21:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0004_alter_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='LittleLemonAPI.category', validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]