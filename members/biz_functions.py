from .models import AttendanceRegister, MemberAttendance
from .models import ChurchMember, MEMBER_STATUSES


def get_present_and_absent_members(attendance_register: AttendanceRegister):
    """Return lists of those absent on the portal for a meeting"""
    marked_attendance = MemberAttendance.objects.filter(register_id=attendance_register.id).values(
        'id', 'member_id', 'is_present')
    listed_member_ids = [item['member_id'] for item in marked_attendance]
    listed_members = [member for member in ChurchMember.objects.filter(pk__in=listed_member_ids)]

    all_members = ChurchMember.objects.filter(member_status__in=('NEW CONVERT', 'FULL MEMBER')).values()

    absent_members = [member for member in all_members if member['id'] not in listed_member_ids]

    return listed_members, absent_members


def get_present_and_absent_members_for_report(attendance_register: AttendanceRegister):
    """Return lists of those absent for a meeting"""
    present_members = [item.member for item in attendance_register.attendance_items.all() if item.is_present]
    absent_members = [item.member for item in attendance_register.attendance_items.all() if not item.is_present]
    return present_members, absent_members


def get_church_members():
    """Return lists members who are full members or new converts"""

    all_members = ChurchMember.objects.filter(member_status__in=('NEW CONVERT', 'FULL MEMBER')).values()
    all_members = [ChurchMember.objects.get(id=member['id']) for member in all_members.all() ]
    all_members.sort(key=lambda x: x.first_name)

    return all_members


def get_church_members_summary():
    all_members = ChurchMember.objects.filter(member_status__in=('NEW CONVERT', 'FULL MEMBER')).all()
    new_convert_count = len([member for member in all_members if member.member_status == 'NEW CONVERT'])
    full_member_count = len([member for member in all_members if member.member_status == 'FULL MEMBER'])

    return new_convert_count, full_member_count



