# Generated by Django 4.0.6 on 2023-01-28 15:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_churchgroup_churchmember_church_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='churchgroup',
            name='group_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='memberattendance',
            name='register',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_items', to='members.attendanceregister'),
        ),
        migrations.CreateModel(
            name='GroupAttendanceRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateField(default=datetime.date.today)),
                ('attendance_type', models.CharField(choices=[('SUNDAY SERVICE', 'SUNDAY SERVICE'), ('FRIDAY SERVICE', 'FRIDAY SERVICE')], default='SUNDAY SERVICE', max_length=48)),
                ('is_already_synched', models.BooleanField(blank=True, default=False, editable=False, null=True)),
                ('church_group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='members.churchgroup')),
            ],
            options={
                'ordering': ['-date_taken'],
            },
        ),
        migrations.AddField(
            model_name='memberattendance',
            name='group_register',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='attendance_items', to='members.groupattendanceregister'),
        ),
    ]
