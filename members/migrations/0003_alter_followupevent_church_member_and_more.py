# Generated by Django 4.0.6 on 2022-11-05 20:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_rename_present_memberattendance_is_present_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followupevent',
            name='church_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='follow_ups', to='members.churchmember'),
        ),
        migrations.AlterField(
            model_name='followupevent',
            name='follow_up_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
