from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    ISSUE_TYPES = [
        ('pothole', 'Pothole'),
        ('water_leak', 'Water Leak'),
        ('sanitation', 'Sanitation Failure'),
        ('electricity', 'Electricity Fault'),
    ]

    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('PENDING', 'Pending'),
        ('ATTENDED', 'Attended To'),
        ('APPROVED', 'Approved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    admin_comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='reports_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
