# Generated by Django 3.1.3 on 2020-12-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litsource', '0002_auto_20201127_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='literaturesource',
            name='human_name',
            field=models.CharField(default='', max_length=200, verbose_name='Название для показа рядом со ссылками'),
        ),
    ]