from django.contrib.auth.models import User
from django.db import models

BLOOD_GROUPS = [
    ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"),
    ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-"),
]

class DonorProfile(models.Model):
    AVAILABILITY = [("Available", "Available"), ("Not Available", "Not Available")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="donor_profile")
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=150)
    last_donation_date = models.DateField(blank=True, null=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY, default="Available")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.blood_group}"

class BloodRequest(models.Model):
    STATUS = [("Pending", "Pending"), ("Fulfilled", "Fulfilled"), ("Cancelled", "Cancelled")]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blood_requests")
    patient_name = models.CharField(max_length=150)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    hospital_name = models.CharField(max_length=200)
    location = models.CharField(max_length=150)
    required_date = models.DateField()
    bags_required = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["required_date", "-created_at"]

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group}"
