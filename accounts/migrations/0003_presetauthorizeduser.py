# Generated by Django 2.1.2 on 2018-10-27 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181027_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreSetAuthorizedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=70)),
                ('last_name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=15)),
                ('type', models.CharField(choices=[('employee', 'Employee'), ('admin', 'Admin'), ('superuser', 'Superuser')], max_length=20)),
            ],
        ),
    ]
