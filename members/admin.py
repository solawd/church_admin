import io
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.options import TabularInline
from django.http import HttpResponse
from .pdf_utils import generate_multiple_attendance_pdfs, generate_membership_pdf
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

admin.site.site_header = 'NECI Administration'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('first_name', 'last_name', 'email',)


class CustomChurchMemberAdmin(admin.ModelAdmin):
    model = ChurchMember
    list_display = ('first_name', 'middle_name', 'surname', 'member_status',)
    list_filter = ('first_name', 'middle_name', 'surname', 'member_status',)
    search_fields = ['first_name', 'middle_name', 'surname']
    ordering = ('first_name', 'middle_name', 'surname',)


class MemberAttendanceAdminInline(TabularInline):
    extra = 1
    model = MemberAttendance

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_add_related = True
            formfield.widget.can_view_related = False

        return formfield


class FollowUpAdminInline(TabularInline):
    extra = 1
    model = FollowUpEvent

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_add_related = True
            formfield.widget.can_view_related = False

        return formfield


def export_registers_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    registers_query = queryset.values()
    registers = [AttendanceRegister.objects.get(id=register['id']) for register in registers_query]
    file_name = 'AttendanceRegisters'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(file_name)
    buffer = io.BytesIO()
    pdf = generate_multiple_attendance_pdfs(registers, buffer)

    response.write(pdf)
    return response


export_registers_to_pdf.short_description = 'Generate Register PDFs'


def export_members_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    members_query = queryset.values()
    file_name = 'MembershipRegister'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(file_name)
    buffer = io.BytesIO()
    pdf = generate_membership_pdf(buffer)

    response.write(pdf)
    return response


export_members_to_pdf.short_description = 'Generate All Members PDF'


@admin.register(AttendanceRegister)
class AttendanceRegisterModelAdmin(admin.ModelAdmin):
    inlines = (MemberAttendanceAdminInline,)
    fields = ('date_taken', 'attendance_type')
    actions = (export_registers_to_pdf, )

    def response_add(self, request, obj, post_url_continue=None):
        from members.biz_functions import get_present_and_absent_members

        if obj.is_already_synched:
            # register already synched, return to prevent future members from being marked absent
            return super().response_add(request, obj, post_url_continue)

        _, absent_members = get_present_and_absent_members(obj)
        attendance_items = []
        for member in absent_members:
            attendance = MemberAttendance(member_id=member['id'], is_present=False, register=obj)
            attendance_items.append(attendance)

        MemberAttendance.objects.bulk_create(attendance_items)
        obj.is_already_synched = True
        return super().response_add(request, obj, post_url_continue)


@admin.register(ChurchMember)
class ChurchMemberModelAdmin(admin.ModelAdmin):
    inlines = (FollowUpAdminInline, )
    fields = ('first_name', 'middle_name', 'surname', 'date_of_birth', 'address', 'profession', 'mobile_number',
              'member_status', 'member_photo', 'invited_by')
    list_display = ('first_name', 'middle_name', 'surname', 'member_status',)
    list_filter = ('first_name', 'middle_name', 'surname', 'member_status',)
    search_fields = ['first_name', 'middle_name', 'surname']
    ordering = ('first_name', 'middle_name', 'surname',)
    actions = (export_members_to_pdf, )
    list_per_page = 50


admin.site.register(CustomUser, CustomUserAdmin)


