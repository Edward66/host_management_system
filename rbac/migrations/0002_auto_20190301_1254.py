# Generated by Django 2.1.7 on 2019-03-01 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(default=1, max_length=32, verbose_name='图标'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='title',
            field=models.CharField(max_length=32, verbose_name='菜单名称'),
        ),
    ]