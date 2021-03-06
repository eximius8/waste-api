# Generated by Django 3.1.4 on 2020-12-18 19:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('litsource', '0001_initial'),
        ('chemcomponent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardCategoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Название')),
                ('short_name', models.CharField(default='', max_length=100, verbose_name='Короткое название')),
                ('category1_item', models.CharField(max_length=100, verbose_name='Свойство класса 1')),
                ('category2_item', models.CharField(max_length=100, verbose_name='Свойство класса 2')),
                ('category3_item', models.CharField(max_length=100, verbose_name='Свойство класса 3')),
                ('category4_item', models.CharField(max_length=100, verbose_name='Свойство класса 4')),
            ],
            options={
                'verbose_name': 'Категория классификации',
                'verbose_name_plural': 'Категории классификации',
            },
        ),
        migrations.CreateModel(
            name='HazardValueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='Название')),
                ('short_name', models.CharField(default='', max_length=100, verbose_name='Короткое название')),
                ('bad_val', models.FloatField(verbose_name='Значение больше или меньше которого класс опасности = 1')),
                ('average_val', models.FloatField(verbose_name='Среднее значение')),
                ('good_val', models.FloatField(verbose_name='Значение больше или меньше которого класс опасности = 4')),
            ],
            options={
                'verbose_name': 'Числовой параметр',
                'verbose_name_plural': 'Числовые параметры',
            },
        ),
        migrations.CreateModel(
            name='HazardValueProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prop_float_value', models.FloatField(verbose_name='Числовое значение')),
                ('literature_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value_props', to='litsource.literaturesource', verbose_name='Литература')),
                ('value_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value_props', to='componentprop.hazardvaluetype')),
                ('waste_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value_props', to='chemcomponent.wastecomponent')),
            ],
            options={
                'verbose_name': 'Числовое свойство',
                'verbose_name_plural': 'Числовые свойства',
                'unique_together': {('waste_component', 'value_type')},
            },
        ),
        migrations.CreateModel(
            name='HazardCategoryProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prop_category_value', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)], verbose_name='Класс опасности')),
                ('literature_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_props', to='litsource.literaturesource', verbose_name='Литература')),
                ('value_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_props', to='componentprop.hazardcategorytype')),
                ('waste_component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_props', to='chemcomponent.wastecomponent')),
            ],
            options={
                'verbose_name': 'Свойство классификации',
                'verbose_name_plural': 'Свойства классификации',
                'unique_together': {('waste_component', 'value_type')},
            },
        ),
    ]
