# Generated by Django 4.0.2 on 2022-02-20 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0003_order_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]