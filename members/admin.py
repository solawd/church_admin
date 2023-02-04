import io
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.options import TabularInline
from django.http import HttpResponse, HttpResponseRedirect
from .pdf_utils import generate_multiple_attendance_pdfs, generate_membership_pdf, generate_multiple_group_attendance_pdfs
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupAttendanceRegisterForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html
from .models import *

admin.site.site_header = 'NECI Administration'


class GroupRegisterView(PermissionRequiredMixin, DetailView):
    permission_required = "members.view_churchgroup"
    template_name = "admin/members/churchgroup/group_register.html"
    model = ChurchGroup

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }



def make_users_superusers(modeladmin, request, queryset):
    queryset.update(is_superuser=True, is_staff=True)
    messages.info(request, 'Users converted to super users succesfully')


make_users_superusers.short_description = 'Make Users Superusers'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    actions = (make_users_superusers,)
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
    extra = 0
    model = MemberAttendance
    fields = ('member', 'is_present')

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_add_related = True
            formfield.widget.can_view_related = False

        return formfield


class GroupAttendanceMemberAdminInline(TabularInline):
    extra = 0
    model = MemberAttendance
    fields = ('member', 'is_present')

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_add_related = True
            formfield.widget.can_view_related = False

        return formfield

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ChurchMembersAdminInline(TabularInline):
    extra = 0
    model = ChurchMember
    fields = ['first_name', 'surname', 'mobile_number', 'address']
    readonly_fields = ['first_name', 'surname', 'mobile_number', 'address']

    def formfield_for_dbfield(self, *args, **kwargs):
        formfield = super().formfield_for_dbfield(*args, **kwargs)
        if formfield:
            formfield.widget.can_delete_related = False
            formfield.widget.can_change_related = True
            formfield.widget.can_add_related = True
            formfield.widget.can_view_related = False

        return formfield

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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


def export_group_registers_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    registers_query = queryset.values()
    registers = [GroupAttendanceRegister.objects.get(id=register['id']) for register in registers_query]
    file_name = 'GroupAttendanceRegisters'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(file_name)
    buffer = io.BytesIO()
    pdf = generate_multiple_group_attendance_pdfs(registers, buffer)

    response.write(pdf)
    return response


export_group_registers_to_pdf.short_description = 'Generate Group Register PDFs'


def mark_group_register(modeladmin, request, queryset):
    group_query = queryset.values()[0]
    group = ChurchGroup.objects.get(pk=group_query['id'])
    response = HttpResponseRedirect(group.register_url)
    return response

mark_group_register.short_description = 'Mark Group Register'


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


@admin.register(ChurchGroup)
class ChurchGroupModelAdmin(admin.ModelAdmin):
    inlines = (ChurchMembersAdminInline,)
    fields = ('group_name', 'group_leader', 'group_description',)
    list_display = ('group_name', 'group_leader',)
    actions = (mark_group_register,)

    def show_register_url(self, obj):
        return format_html("<a href='{url}'>Mark Group Register</a>", url=obj.register_url)

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path(
                "<pk>/group_register/",
                self.admin_site.admin_view(self.group_register_view),
                name=view_name,
            ),
            *super().get_urls(),
        ]

    def group_register_view(self, request, pk):
        church_group = ChurchGroup.objects.get(pk=pk)

        members = ChurchMember.objects.filter(church_group=church_group,
                                              member_status__in=('NEW CONVERT', 'FULL MEMBER'))

        if request.method == 'POST':
            form = GroupAttendanceRegisterForm(request.POST, members=members)

            if form.is_valid():
                register_date = form.cleaned_data['register_date']
                attendance_type = form.cleaned_data['attendance_type']

                group_register = GroupAttendanceRegister.objects.filter(church_group=church_group,
                                                                        date_taken=register_date,
                                                                        attendance_type=attendance_type)
                if not group_register:
                    group_register = GroupAttendanceRegister(
                        church_group=church_group,date_taken=register_date
                    )
                    group_register.save()
                    attendances = []
                    for member in members:
                        is_present = form.cleaned_data[f'member_{member.id}']
                        member_attend = MemberAttendance(
                            group_register=group_register,
                            member=member,
                            is_present=is_present
                        )
                        attendances.append(member_attend)
                    MemberAttendance.objects.bulk_create(attendances)
                    messages.info(request, 'Attendance Register successfully recorded')
                    return HttpResponseRedirect(request.path_info)

                else: #register exists for same already
                    messages.error(request, 'There is an existing register for this date already')
                    return HttpResponseRedirect(request.path_info)

        else:
            group_attendance_form = GroupAttendanceRegisterForm(members=members)
            context = dict(
                # Include common variables for rendering the admin template.
                admin.site.each_context(request),
                # Anything else you want in the context...
                group_form=group_attendance_form,
                church_group=church_group,
            )
            return TemplateResponse(request, "admin/members/churchgroup/group_register.html", context)


@admin.register(GroupAttendanceRegister)
class GroupAttendanceRegisterModelAdmin(admin.ModelAdmin):
    inlines = (GroupAttendanceMemberAdminInline,)
    fields = ('church_group', 'date_taken', 'attendance_type')
    search_fields = ['church_group__group_name',]
    actions = (export_group_registers_to_pdf, )


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
              'member_status', 'church_group', 'member_photo', 'invited_by')
    list_display = ('first_name', 'middle_name', 'surname', 'member_status',)
    list_filter = ('first_name', 'middle_name', 'surname', 'member_status',)
    search_fields = ['first_name', 'middle_name', 'surname']
    ordering = ('first_name', 'middle_name', 'surname',)
    actions = (export_members_to_pdf, )
    list_per_page = 50


admin.site.register(CustomUser, CustomUserAdmin)


