# Generated by Django 3.2.5 on 2021-08-06 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order_vendors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='address1',
            field=models.CharField(default=1, max_length=60, verbose_name='Address line 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='address2',
            field=models.CharField(blank=True, max_length=60, verbose_name='Address line 2'),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(choices=[('uk', 'United Kingdom'), ('us', 'United States of America')], default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(default=1, max_length=12, verbose_name='ZIP / Postal code'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
