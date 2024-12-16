# Generated by Django 5.1.3 on 2024-12-10 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PatientVitals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('vitals', models.JSONField()),
                ('softSOS', models.BooleanField(default=False)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eliteapi.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Reminders',
            fields=[
                ('reminder_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('remaining_days', models.IntegerField(default=0)),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eliteapi.patient')),
            ],
        ),
    ]
