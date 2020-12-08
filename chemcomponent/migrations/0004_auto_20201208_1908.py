# Generated by Django 3.1.3 on 2020-12-08 16:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('litsource', '0004_auto_20201208_1908'),
        ('chemcomponent', '0003_auto_20201208_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastecomponent',
            name='land_concentration',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(1000000.0)], verbose_name='Максимальная фоновая концентрация в почвах (мг/кг)'),
        ),
        migrations.AlterField(
            model_name='wastecomponent',
            name='lit_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='waste_components', to='litsource.literaturesource', verbose_name='Источник литературы (если задано числовое значение X, то обязателен)'),
        ),
    ]