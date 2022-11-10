import io
from .models import AttendanceRegister
from django.http import HttpResponse
from .biz_functions import get_present_and_absent_members
from .pdf_utils import generate_attendance_pdf


# Create your views here.
def attendance_register_view(request, register_id):
    """
    Generate PDF for attendance register
    :param register_id:
    :param request:
    :return:
    """
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    attendance_register = AttendanceRegister.objects.get(id=register_id)
    if attendance_register:
        file_name = f'{attendance_register.attendance_type}-{str(attendance_register.date_taken)}'
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(file_name)

        buffer = io.BytesIO()
        present_members, absent_members = get_present_and_absent_members(attendance_register)
        pdf = generate_attendance_pdf(attendance_register, buffer, present_members, absent_members)

        response.write(pdf)
        return response
        # return FileResponse(buffer, as_attachment=True, filename=file_name)

