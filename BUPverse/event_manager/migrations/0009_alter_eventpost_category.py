# Generated by Django 5.2 on 2025-07-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0008_alter_recom_choose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='category',
            field=models.CharField(choices=[('Tech', 'Tech'), ('Business', 'Business'), ('CP', 'Competitive programming'), ('Debate', 'Debate'), ('Hackathon', 'Hackathon'), ('CTF', 'Capture The Flag'), ('Cultural', 'Culture'), ('Career', 'Career / Skill'), ('Social', 'Social Work'), ('Research', 'Research / Academic'), ('Sports', 'Sports'), ('General', 'General'), ('Workshop', 'Workshop'), ('Others', 'Others'), ('', '')], default='', max_length=20),
        ),
    ]
