import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

MEMBER_STATUSES = (('VISITOR', 'VISITOR'),
                   ('NEW CONVERT', 'NEW CONVERT'),
                   ('FULL MEMBER', 'FULL MEMBER'))

FELLOWSHIPS = (('CHILDREN', 'CHILDREN'),
               ('YOUTH', 'YOUTH'),
               ('MEN', 'MEN'),
               ('WOMEN', 'WOMEN'))

ATTENDANCE_TYPES = (('SUNDAY SERVICE', 'SUNDAY SERVICE'),
               ('FRIDAY SERVICE', 'FRIDAY SERVICE'))


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    objects = CustomUserManager()

    def __str__(self):
        return f'[ {self.first_name} {self.last_name} ]'


class ChurchMember(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=1000)
    profession = models.CharField(max_length=1000)
    mobile_number = models.CharField(max_length=32)
    member_status = models.CharField(max_length=15, choices=MEMBER_STATUSES, default="VISITOR")

    photo_width = models.PositiveIntegerField(null=True, blank=True)
    photo_height = models.PositiveIntegerField(null=True, blank=True)
    member_photo = models.ImageField(upload_to='photos/', height_field='photo_height', width_field='photo_width',
                                   max_length=2000, null=True, blank=True)
    invited_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.first_name.upper()} {self.middle_name.upper()} {self.surname.upper()}'


class FollowUpEvent(models.Model):
    undertaken_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.DO_NOTHING)
    church_member = models.ForeignKey(ChurchMember, on_delete=models.DO_NOTHING, related_name='follow_ups')
    follow_up_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    follow_up_notes = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f'[ {self.follow_up_date}: {self.church_member.first_name} {self.church_member.surname} ]'


class AttendanceRegister(models.Model):
    date_taken = models.DateField(default=datetime.date.today)
    attendance_type = models.CharField(max_length=48, choices=ATTENDANCE_TYPES, default='SUNDAY SERVICE')

    def __str__(self):
        return f'[ {self.attendance_type} : {self.date_taken} ]'



class MemberAttendance(models.Model):
    register = models.ForeignKey(AttendanceRegister, on_delete=models.DO_NOTHING, related_name='attendance_items')
    member = models.ForeignKey(ChurchMember, on_delete=models.DO_NOTHING)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        if self.is_present:
            return f'[ {self.register} - {self.member} - Present ]'
        return f'[ {self.register} - {self.member} - Absent ]'
