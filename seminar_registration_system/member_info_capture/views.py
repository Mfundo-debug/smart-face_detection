from django.shortcuts import render,redirect
from member_info_capture.models import Member
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

def member_info_capture(request):
    if request.method == 'POST':
        student_type = request.POST.get('student_type')
        last_name = request.POST.get('last_name')
        first_names = request.POST.get('first_names')
        personal_email = request.POST.get('personal_email')
        student_id = request.POST.get('student_id')
        residential_address = request.POST.get('residential_address')
        member = Member(
            student_type=student_type,
            last_name=last_name,
            first_names=first_names,
            personal_email=personal_email,
            student_id=student_id,
            residential_address=residential_address,
        )
        member.save()
        messages.success(request, 'Member added successfully')
        #Redirect to the admin page after saving member's information
        return redirect(reverse('admin: member_info_capture_member_change', args=[member.id]))
    #Handle GET requests
    return redirect('member_info_capture')

def find_user(request):
    if request.method == 'POST':
        user_number = request.POST.get('user_number')
        try:
            member = Member.objects.get(user_number=user_number)
            return redirect(reverse('admin: member_info_capture_member_change', args=[member.id]))
        except Member.DoesNotExist:
            messages.error(request, 'Member with user number {} does not exist'.format(user_number))
            return redirect('member_info_capture')
        except ValueError:
            messages.error(request, 'Invalid user number')
            return redirect('member_info_capture')
    #Handle GET requests
    return HttpResponse('/')

def landing_page(request):
    return render(request, 'member_info_capture/landing_page.html')

