# Generated by Django 2.1.2 on 2019-03-02 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_sheet', '0011_remove_timesheet_creator_signature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='address',
            field=models.CharField(blank=True, help_text='**Change if address mobile', max_length=150, null=True),
        ),
    ]