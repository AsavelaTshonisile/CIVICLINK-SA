from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report-issue/', views.report_issue, name='report_issue'),
    path('check-status/', views.check_status, name='check_status'),
    path('update-status/<int:report_id>/', views.update_status, name='update_status'),
]
