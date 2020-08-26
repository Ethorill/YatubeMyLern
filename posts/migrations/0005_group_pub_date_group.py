# Generated by Django 2.2.9 on 2020-05-21 14:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200521_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='pub_date_group',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='date published_group'),
            preserve_default=False,
        ),
    ]