# Generated by Django 2.1.2 on 2019-03-02 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_sheet', '0010_auto_20190302_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesheet',
            name='creator_signature',
        ),
    ]