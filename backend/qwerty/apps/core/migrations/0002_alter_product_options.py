# Generated by Django 3.2.7 on 2021-09-21 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('category', 'name')},
        ),
    ]