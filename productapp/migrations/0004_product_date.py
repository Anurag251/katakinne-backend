# Generated by Django 4.1 on 2022-12-14 07:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0003_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 12, 14, 7, 5, 55, 40785, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
