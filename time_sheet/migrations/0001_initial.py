# Generated by Django 2.1.2 on 2018-10-30 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('lunch', models.CharField(choices=[('half-hour', 'Half Hour'), ('hour', 'Hour'), ('none', 'None')], max_length=20)),
                ('injured', models.BooleanField()),
                ('comment', models.TextField()),
                ('signature', models.CharField(max_length=50)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=100)),
                ('job_num', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(choices=[('Single', 'Single'), ('Ongoing', 'Ongoing'), ('ER', 'ER')], max_length=20)),
                ('completed', models.BooleanField()),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supervisor_sig', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Incomplete', 'Incomplete'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Complete', 'Complete')], max_length=20)),
                ('employee_works', models.ManyToManyField(blank=True, null=True, to='time_sheet.EmployeeWork')),
                ('receipts', models.ManyToManyField(blank=True, null=True, to='time_sheet.Receipt')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=150)),
                ('completed', models.BooleanField()),
                ('time_sheet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='time_sheet.TimeSheet')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='workdays',
            field=models.ManyToManyField(blank=True, null=True, to='time_sheet.WorkDay'),
        ),
    ]
