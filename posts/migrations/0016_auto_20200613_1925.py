# Generated by Django 2.2.9 on 2020-06-13 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20200525_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='user',
                to=settings.AUTH_USER_MODEL),
        ),
    ]