# Generated by Django 3.2 on 2022-07-14 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0023_level_desig_desig_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='HRMS',
            fields=[
                ('hrms_employee_id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('ipas_employee_id', models.CharField(max_length=15)),
                ('employee_first_name', models.CharField(max_length=150, null=True)),
                ('employee_middle_name', models.CharField(max_length=150, null=True)),
                ('employee_last_name', models.CharField(max_length=150, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('community_sr', models.CharField(max_length=3, null=True)),
                ('official_mobile_no', models.CharField(max_length=10, null=True)),
                ('official_email_id', models.CharField(max_length=50, null=True)),
                ('designation', models.CharField(max_length=300, null=True)),
                ('railway_group', models.CharField(max_length=1, null=True)),
                ('current_zone', models.CharField(max_length=10)),
                ('current_unit_division', models.CharField(max_length=80, null=True)),
                ('current_place', models.CharField(max_length=100, null=True)),
                ('department', models.CharField(max_length=50, null=True)),
                ('sub_department', models.CharField(max_length=50, null=True)),
                ('service_status', models.CharField(max_length=50, null=True)),
                ('billunit', models.CharField(max_length=7, null=True)),
                ('paylevel', models.CharField(max_length=4, null=True)),
                ('emptype', models.CharField(max_length=100, null=True)),
                ('appointment_date', models.DateField(null=True)),
                ('superannuation_date', models.DateField(null=True)),
                ('txn_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]