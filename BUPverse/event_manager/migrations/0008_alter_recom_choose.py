# Generated by Django 5.2 on 2025-06-24 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0007_alter_recom_choose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recom',
            name='choose',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4 '), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=10),
        ),
    ]
