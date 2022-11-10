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
