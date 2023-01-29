from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ChurchMember, AttendanceRegister


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class AttendanceRegisterForm(forms.ModelForm):

    class Meta:
        model = AttendanceRegister
        fields = ('date_taken', 'attendance_type',)


class GroupAttendanceRegisterForm(forms.Form):
    from members.models import ATTENDANCE_TYPES
    register_date = forms.DateField(widget=forms.SelectDateWidget, label='Attendance Date')
    attendance_type = forms.ChoiceField(choices=ATTENDANCE_TYPES, label='Attendance Type')

    def __init__(self, *args, **kwargs):

        members = kwargs.pop('members', [])

        super(GroupAttendanceRegisterForm, self).__init__(*args, **kwargs)

        for member in members:
            # generate extra fields in the number specified via extra_fields
            self.fields['member_{index}'.format(index=member.id)] = \
                forms.BooleanField(label=f'{member.first_name} {member.surname}', initial=False, required=False)

    def get_member_fields(self):
        for field_name in self.fields:
            if field_name.startswith('member_'):
                yield self[field_name]
