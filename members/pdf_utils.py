import datetime
import io
from .models import AttendanceRegister
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, HRFlowable


def generate_attendance_pdf(attendance_register: AttendanceRegister, buffer: io.BytesIO,
                            present_members: [], absent_members: []):

    doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72
            )
    table_width = doc.width
    flowables = []
    title_style = ParagraphStyle(
        name='title',
        fontSize=14,
        leading=14,
    )
    h_line = HRFlowable(width="80%", thickness=1, lineCap='round',
                        color='lightgrey', spaceBefore=1, spaceAfter=1,
                        hAlign='CENTER', vAlign='BOTTOM', dash=None)
    heading_style = ParagraphStyle(
        name='title',
        fontSize=12,
        leading=12,
    )
    title = f"<br/><br/>Attendance Register : {attendance_register.attendance_type} {attendance_register.date_taken.strftime('%d-%m-%Y')} <br/><br/>"
    document_title = Paragraph(title, style=title_style)
    flowables.append(document_title)
    flowables.append(h_line)

    # Present Members
    present_title = Paragraph(f'<br/><br/>[ Members Present ] <br/><br/>', style=heading_style)
    flowables.append(present_title)
    present_members_data = []
    headings = ['Member Name', 'Member Status', 'Present/Absent']
    present_members_data.append(headings)
    for member in present_members:
        present_members_data.append([f'{member.first_name} {member.surname}', member.member_status, 'Present'])

    table_style = TableStyle(
        [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue)])
    tbl = Table(present_members_data, colWidths=[table_width/3, table_width/3, table_width/3], hAlign='LEFT')
    tbl.setStyle(table_style)
    flowables.append(tbl)

    # Absent Members
    absent_title = Paragraph('<br/><br/>[ Members Absent ]<br/><br/>', style=heading_style)
    flowables.append(absent_title)
    absent_members_data = []
    headings = ['Member Name', 'Member Status', 'Present/Absent']
    absent_members_data.append(headings)
    for member in absent_members:
        absent_members_data.append([f"{member['first_name']} {member['surname']}", member['member_status'], 'Absent'])

    tbl2 = Table(absent_members_data, colWidths=[table_width/3, table_width/3, table_width/3], hAlign='LEFT')
    tbl2.setStyle(table_style)
    flowables.append(tbl2)

    doc.build(flowables)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_multiple_attendance_pdfs(attendance_registers: [AttendanceRegister], buffer: io.BytesIO):
    from .biz_functions import get_present_and_absent_members_for_report
    doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72
            )
    table_width = doc.width
    flowables = []
    title_style = ParagraphStyle(
        name='title',
        fontSize=14,
        leading=14,
    )
    heading_style = ParagraphStyle(
        name='title',
        fontSize=12,
        leading=12,
    )
    h_line = HRFlowable(width="90%", thickness=1, lineCap='round',
                        color='lightgrey', spaceBefore=1, spaceAfter=1,
                        hAlign='LEFT', vAlign='BOTTOM', dash=None)

    # Present Members
    for attendance_register in attendance_registers:
        title = f"<br/><br/>Attendance Register : {attendance_register.attendance_type} {attendance_register.date_taken.strftime('%d-%m-%Y')} <br/><br/>"
        document_title = Paragraph(title, style=title_style)
        flowables.append(document_title)
        flowables.append(h_line)
        present_members, absent_members = get_present_and_absent_members_for_report(attendance_register)
        visitors_count = len([member for member in present_members if member.member_status == 'VISITOR'])
        present_title = Paragraph(f'<br/><br/>[ Members Present ] <br/><br/>', style=heading_style)
        flowables.append(present_title)
        present_members_data = []
        headings = ['Member Name', 'Member Status', 'Present/Absent']
        present_members_data.append(headings)
        for member in present_members:
            present_members_data.append([f'{member.first_name} {member.surname}', member.member_status, 'Present'])

        table_style = TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue)])
        tbl = Table(present_members_data, colWidths=[table_width/3, table_width/3, table_width/3], hAlign='LEFT')
        tbl.setStyle(table_style)
        flowables.append(tbl)

        # Absent Members
        absent_title = Paragraph('<br/><br/>[ Members Absent ]<br/><br/>', style=heading_style)
        flowables.append(absent_title)
        absent_members_data = []
        headings = ['Member Name', 'Member Status', 'Present/Absent']
        absent_members_data.append(headings)
        for member in absent_members:
            absent_members_data.append([f'{member.first_name} {member.surname}', member.member_status, 'Absent'])

        tbl2 = Table(absent_members_data, colWidths=[table_width/3, table_width/3, table_width/3], hAlign='LEFT')
        tbl2.setStyle(table_style)
        flowables.append(tbl2)

        # Summary Section
        summary_title = Paragraph('<br/><br/><br/>Attendance Summary <br/><br/>', style=heading_style)
        summary_body = Paragraph(f"""<br/>Members Present : {len(present_members)}<br/><br/>
                                Members Absent: {len(absent_members)}<br/><br/>
                                Visitors Present: {visitors_count} """, style=heading_style)
        flowables.append(summary_title)
        flowables.append(h_line)
        flowables.append(summary_body)
        flowables.append(PageBreak())

    doc.build(flowables)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_membership_pdf(buffer: io.BytesIO):
    from .biz_functions import get_church_members, get_church_members_summary
    doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72
            )
    table_width = doc.width
    flowables = []
    title_style = ParagraphStyle(
        name='title',
        fontSize=14,
        leading=14,
    )
    heading_style = ParagraphStyle(
        name='title',
        fontSize=12,
        leading=12,
    )
    h_line = HRFlowable(width="90%", thickness=1, lineCap='round',
                        color='lightgrey', spaceBefore=1, spaceAfter=1,
                        hAlign='LEFT', vAlign='BOTTOM', dash=None)

    church_members = get_church_members()
    new_cvt_count, full_member_count = get_church_members_summary()
    title = f"<br/><br/>NECI Membership Register : {datetime.datetime.now().strftime('%d-%m-%Y')} <br/><br/>"
    document_title = Paragraph(title, style=title_style)
    flowables.append(document_title)
    flowables.append(h_line)
    flowables.append(Paragraph('<br/><br/>'))

    members_data = []
    headings = ['Member Name', 'Member Status', 'Mobile Number', "Profession"]
    members_data.append(headings)
    for member in church_members:
        members_data.append([f'{member.first_name} {member.surname}', member.member_status,
                                     member.mobile_number, member.profession])

    table_style = TableStyle(
        [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue)])
    tbl = Table(members_data, colWidths=[table_width/4, table_width/4, table_width/4, table_width/4], hAlign='LEFT')
    tbl.setStyle(table_style)
    flowables.append(tbl)

    # Summary
    summary_total = Paragraph(f'<br/>Total: {len(church_members)}<br/>')
    summary_new_converts = Paragraph(f'<br/>New Converts Count: {new_cvt_count}<br/>')
    summary_full_count = Paragraph(f'<br/>Full Members Count: {full_member_count}<br/>')

    summary_title = Paragraph(f'<br/><br/>Summary<br/><br/>', style=heading_style)
    flowables.append(summary_title)
    flowables.append(h_line)
    flowables.append(summary_total)
    flowables.append(summary_new_converts)
    flowables.append(summary_full_count)

    doc.build(flowables)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


# Action for exporting registers to PDFs
def attendance_register_view(modeladmin, request, queryset):
    """
    Generate PDF for attendance register
    :param register_id:
    :param request:
    :return:
    """
    # Create a file-like buffer to receive PDF data.
    from .biz_functions import get_present_and_absent_members
    from django.http import HttpResponse

    response = HttpResponse(content_type='application/pdf')
    registers_query = queryset.values()
    registers = [AttendanceRegister.objects.get(id=register['id']) for register in registers_query]
    file_name = 'AttendanceRegisters'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(file_name)
    buffer = io.BytesIO()
    pdf = generate_multiple_attendance_pdfs(registers, buffer)

    response.write(pdf)
    return response

