# Generated by Django 4.0.6 on 2022-12-03 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_followupevent_church_member_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendanceregister',
            options={'ordering': ['-date_taken']},
        ),
        migrations.AlterModelOptions(
            name='churchmember',
            options={'ordering': ['first_name', 'surname']},
        ),
        migrations.AlterModelOptions(
            name='followupevent',
            options={'ordering': ['-follow_up_date']},
        ),
    ]
