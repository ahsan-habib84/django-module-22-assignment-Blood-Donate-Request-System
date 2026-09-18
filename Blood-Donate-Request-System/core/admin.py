from django.contrib import admin
from .models import DonorProfile, BloodRequest

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "blood_group", "phone", "location", "availability", "last_donation_date")
    list_filter = ("blood_group", "availability", "location")
    search_fields = ("user__username", "user__first_name", "user__last_name", "location")

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "blood_group", "hospital_name", "location", "required_date", "bags_required", "status")
    list_filter = ("blood_group", "status", "location")
    search_fields = ("patient_name", "hospital_name", "location")
