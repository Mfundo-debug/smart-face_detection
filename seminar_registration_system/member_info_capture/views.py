from django.shortcuts import render,redirect
from .models import Member

def member_info_capture(request):
    if request.method == 'POST':
        student_type = request.POST.get('student_type')
        last_name = request.POST.get('last_name')
        first_names = request.POST.get('first_name')
        personal_email = request.POST.get('personal_email')
        student_id = request.POST.get('student_id')
        residential_address = request.POST.get('residential_address')
        member = Member(
            student_type=student_type,
            last_name=last_name,
            first_name=first_names,
            personal_email=personal_email,
            student_id=student_id,
            residential_address=residential_address,
        )
        member.save()
        return redirect('member_info_capture_success')
    return render(request, 'member_info_capture/templates/member_info_capture.html')

def member_info_capture_success(request):
    return render(request, 'member_info_capture/templates/member_info_capture_success.html')
