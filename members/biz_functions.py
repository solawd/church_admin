from .models import AttendanceRegister
from .models import ChurchMember, MEMBER_STATUSES


def get_present_and_absent_members(attendance_register: AttendanceRegister):
    """Return lists of those absent for a meeting"""
    present_member_ids = [item.member.id for item in attendance_register.attendance_items.all()]
    present_members = [item.member for item in attendance_register.attendance_items.all()]

    all_members = ChurchMember.objects.filter(member_status='NEW CONVERT').values() | \
                  ChurchMember.objects.filter(member_status='FULL MEMBER').values()

    absent_members = [member for member in all_members.all() if member['id'] not in present_member_ids]

    return present_members, absent_members


def get_church_members():
    """Return lists members who are full members or new converts"""

    all_members = ChurchMember.objects.filter(member_status='NEW CONVERT').values() | \
                  ChurchMember.objects.filter(member_status='FULL MEMBER').values()

    all_members = [ChurchMember.objects.get(id=member['id']) for member in all_members.all() ]
    all_members.sort(key=lambda x: x.first_name)

    return all_members




