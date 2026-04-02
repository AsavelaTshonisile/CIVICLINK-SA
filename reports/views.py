from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Report
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def dashboard(request):
    if request.user.is_staff:
        all_reports = Report.objects.exclude(status='APPROVED').order_by('-created_at')
        return render(request, 'reports/admin_dashboard.html', {
            'reports': all_reports,
            'status_choices': Report.STATUS_CHOICES
        })
    return render(request, 'reports/dashboard.html')

@login_required
def update_status(request, report_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not authorized.")
    if request.method == 'POST':
        report = get_object_or_404(Report, id=report_id)
        new_status = request.POST.get('status')
        admin_comment = request.POST.get('admin_comment')
        
        if new_status:
            report.status = new_status
        if admin_comment is not None:
            report.admin_comment = admin_comment
            
        report.save()
        messages.success(request, f"Status and comment for '{report.title}' updated successfully.")
    return redirect('dashboard')

@login_required
def report_issue(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        issue_type = request.POST.get('issue_type')
        location = request.POST.get('location')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        
        if title and issue_type and location and description:
            Report.objects.create(
                user=request.user,
                title=title,
                issue_type=issue_type,
                location=location,
                description=description,
                photo=photo
                # status defaults to 'SUBMITTED'
            )
            messages.success(request, 'Your issue has been successfully reported.')
            return redirect('check_status')
        else:
            messages.error(request, 'Please fill in all the required fields.')
            
    issue_types = Report.ISSUE_TYPES
    return render(request, 'reports/report_form.html', {'issue_types': issue_types})

@login_required
def check_status(request):
    reports = Report.objects.filter(user=request.user).exclude(status='APPROVED').order_by('-created_at')
    return render(request, 'reports/status_list.html', {'reports': reports})
