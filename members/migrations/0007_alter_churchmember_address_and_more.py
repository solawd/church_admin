# Generated by Django 4.0.6 on 2022-12-04 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_attendanceregister_is_already_synched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='churchmember',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='churchmember',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='churchmember',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='churchmember',
            name='profession',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
