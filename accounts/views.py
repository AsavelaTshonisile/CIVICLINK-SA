from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib import messages
from reports.models import Report

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_reports = Report.objects.count()
        if total_reports > 0:
            context['approved_count'] = int((Report.objects.filter(status='APPROVED').count() / total_reports) * 100)
            context['pending_count'] = int((Report.objects.filter(status='PENDING').count() / total_reports) * 100)
            context['attended_count'] = int((Report.objects.filter(status='ATTENDED').count() / total_reports) * 100)
        else:
            context['approved_count'] = 0
            context['pending_count'] = 0
            context['attended_count'] = 0
        return context

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to CIVICLINK SA!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
