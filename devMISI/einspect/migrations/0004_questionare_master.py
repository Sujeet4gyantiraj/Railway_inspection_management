# Generated by Django 3.2 on 2022-08-23 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0046_category'),
        ('einspect', '0003_choicetype_master_dropdown_options_radio_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='questionare_master',
            fields=[
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('activity', models.CharField(max_length=200)),
                ('created_by', models.CharField(blank=True, max_length=20, null=True)),
                ('lastmodified_by', models.CharField(blank=True, max_length=20, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('lastmodified_on', models.DateTimeField(auto_now=True)),
                ('delete_flag', models.BooleanField(default=False)),
                ('choicetype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='einspect.choicetype_master')),
                ('doption', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='einspect.dropdown_options')),
                ('instypeid_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.inspectiontype_master')),
                ('roption1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='firstOption', to='einspect.radio_options')),
                ('roption2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondOption', to='einspect.radio_options')),
            ],
        ),
    ]