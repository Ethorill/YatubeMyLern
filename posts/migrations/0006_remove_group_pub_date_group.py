# Generated by Django 2.2.9 on 2020-05-21 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_group_pub_date_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='pub_date_group',
        ),
    ]
