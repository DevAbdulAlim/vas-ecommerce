# Generated by Django 4.2.6 on 2023-10-31 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]