# Generated by Django 4.2.11 on 2024-03-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_currency_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
    ]
