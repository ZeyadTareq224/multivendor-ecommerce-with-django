# Generated by Django 3.2.5 on 2021-07-31 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
