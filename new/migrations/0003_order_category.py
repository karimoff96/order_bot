# Generated by Django 4.0.2 on 2022-02-20 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('new', '0002_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
