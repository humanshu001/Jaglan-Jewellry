# Generated by Django 4.2.3 on 2023-08-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_feedback_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feedback',
            field=models.TextField(null=True),
        ),
    ]
