# Generated by Django 4.2.3 on 2023-08-21 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_qty',
            field=models.IntegerField(default=1),
        ),
    ]
