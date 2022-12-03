from django.db.models.signals import post_save
from django.dispatch import receiver
from members.models import AttendanceRegister, MemberAttendance
from members.biz_functions import get_present_and_absent_members

#
# @receiver(post_save, sender=AttendanceRegister)
# def sync_attendance_registration(sender, instance, created, **kwargs):
#     """Sync the attendance register and add all church members not on it as absent"""
#     if not created:
#         return
#     _, absent_members = get_present_and_absent_members(instance)
#     attendance_items = []
#     for member in absent_members:
#         attendance = MemberAttendance(member_id=member['id'], is_present=False, register=instance)
#         attendance_items.append(attendance)
#
#     MemberAttendance.objects.bulk_create(attendance_items)
