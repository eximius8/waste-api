# Generated by Django 3.1.2 on 2020-10-11 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chemcomponent', '0002_wastecomponent_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardProp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prop_type', models.PositiveSmallIntegerField(choices=[(1, 'ПДК (ОДК) в почве, мг/кг'), (2, 'ПДК (ОДУ) в воде, мг/л'), (3, 'ПДК рабочей зоны, мг/м^3'), (4, 'ПДК среднесуточная или максимально разовая (ОБУВ), мг/м^3'), (5, 'Класс опасности в воде'), (6, 'Класс опасности в рабочей зоне'), (7, 'Класс опасности в атмосферном воздухе'), (8, 'Класс опасности в почве'), (9, 'DL50 перорально, мг/кг'), (10, 'CL50, мг/м^3'), (11, 'Канцерогенность'), (12, 'Lg (S, мг/л/ПДКв)'), (13, 'Lg (Снас, мг/м^3/ПДКр. з)'), (14, 'ПДКвр, мг/л'), (15, 'DL50skin, мг/кг '), (16, 'CL50w, мг/л/96 ч '), (17, 'Lg (Снас, мг/м^3/ПДКсс/мр)'), (18, 'КВИО'), (19, 'Log Kow (октанол/вода)'), (20, 'Персистентность: трансформация в окружающей среде'), (21, 'Биоаккумуляция: поведение в пищевой цепочке'), (22, 'Мутагенность'), (23, 'ПДКпп в продуктах питания')])),
                ('prop_float_value', models.FloatField(blank=True, null=True)),
                ('prop_class_value', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 класс'), (2, '2 класс'), (3, '3 класс'), (4, '4 класс')], null=True)),
                ('prop_cancerog_value', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Доказана для человека'), (2, 'Доказана для животных'), (3, 'Есть вероятность для животных'), (4, 'Неканцероген (доказано)')], null=True, verbose_name='Класс опасности')),
                ('prop_presist_value', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Образование болеетоксичных продуктов, в т.ч. обладающих отдаленными эффектами или новыми свойствами'), (2, 'Образование продуктов с более выраженным влиянием др. критериев вредности'), (3, 'Образование продуктов, токсичность которых близка к токсичности исходного вещества'), (4, 'Образование менее токсичных продуктов')], null=True, verbose_name='Персистентность: трансформация в окружающей среде')),
                ('prop_bioacc_value', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Накопление во всех звеньях'), (2, 'Накопление в нескольких звеньях'), (3, 'Накопление в одном из звеньев'), (4, 'Нет накопления')], null=True, verbose_name='Биоаккумуляция: поведение в пищевой цепочке')),
                ('prop_mutag_value', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Обнаружена'), (2, 'Есть возможность проявления для человека'), (3, 'Есть возможность проявления для животных'), (4, 'Отсутствует (доказано) ')], null=True, verbose_name='Мутагенность')),
                ('literature_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemcomponent.literaturesource')),
            ],
        ),
        migrations.RemoveField(
            model_name='cancerogprop',
            name='literature_source',
        ),
        migrations.RemoveField(
            model_name='cancerogprop',
            name='waste_component',
        ),
        migrations.RemoveField(
            model_name='hazardclassprop',
            name='literature_source',
        ),
        migrations.RemoveField(
            model_name='hazardclassprop',
            name='waste_component',
        ),
        migrations.RemoveField(
            model_name='hazardvalueprop',
            name='literature_source',
        ),
        migrations.RemoveField(
            model_name='hazardvalueprop',
            name='waste_component',
        ),
        migrations.RemoveField(
            model_name='mutagenprop',
            name='literature_source',
        ),
        migrations.RemoveField(
            model_name='mutagenprop',
            name='waste_component',
        ),
        migrations.RemoveField(
            model_name='persistprop',
            name='literature_source',
        ),
        migrations.RemoveField(
            model_name='persistprop',
            name='waste_component',
        ),
        migrations.AlterModelOptions(
            name='wastecomponent',
            options={'verbose_name': 'Компонент отхода'},
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='bio_acc_prop',
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='cancerog_prop',
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='hazard_class_prop',
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='hazard_value_prop',
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='mutagen_prop',
        ),
        migrations.RemoveField(
            model_name='wastecomponent',
            name='persist_prop',
        ),
        migrations.AlterField(
            model_name='wastecomponent',
            name='chemical_type',
            field=models.CharField(choices=[('S', 'Неопасное W=10^6'), ('O', 'Органическое'), ('I', 'Неорганическое')], default='S', max_length=1, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='wastecomponent',
            name='name',
            field=models.CharField(max_length=400, verbose_name='Название'),
        ),
        migrations.DeleteModel(
            name='BioAccProp',
        ),
        migrations.DeleteModel(
            name='CancerogProp',
        ),
        migrations.DeleteModel(
            name='HazardClassProp',
        ),
        migrations.DeleteModel(
            name='HazardValueProp',
        ),
        migrations.DeleteModel(
            name='MutagenProp',
        ),
        migrations.DeleteModel(
            name='PersistProp',
        ),
        migrations.AddField(
            model_name='hazardprop',
            name='waste_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chemcomponent.wastecomponent'),
        ),
        migrations.AddField(
            model_name='wastecomponent',
            name='hazard_prop',
            field=models.ManyToManyField(related_name='hazard_prop', through='chemcomponent.HazardProp', to='chemcomponent.LiteratureSource'),
        ),
    ]
