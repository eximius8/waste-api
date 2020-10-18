# Generated by Django 3.1.2 on 2020-10-13 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemcomponent', '0002_auto_20201012_1046'),
        ('waste', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='concentration',
            name='conc_p',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='wasteclass',
            name='fkko',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Код ФККО'),
        ),
        migrations.AlterUniqueTogether(
            name='concentration',
            unique_together={('waste', 'component')},
        ),
    ]