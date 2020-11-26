# Generated by Django 3.1.3 on 2020-11-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemcomponent', '0002_auto_20201012_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='wastecomponent',
            name='other_names',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Другие названия (через запятую)'),
        ),
        migrations.AlterField(
            model_name='wastecomponent',
            name='chemical_type',
            field=models.CharField(choices=[('O', 'Органическое'), ('I', 'Неорганическое')], default='O', max_length=1, verbose_name='Тип'),
        ),
    ]