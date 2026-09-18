from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm, DonorForm, BloodRequestForm, ProfileForm
from .models import DonorProfile, BloodRequest

def home(request):
    return render(request, "core/home.html", {
        "donor_count": DonorProfile.objects.filter(availability="Available").count(),
        "request_count": BloodRequest.objects.filter(status="Pending").count(),
    })

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "core/profile.html", {"form": form})

def donor_list(request):
    donors = DonorProfile.objects.select_related("user").all()
    blood_group = request.GET.get("blood_group", "")
    location = request.GET.get("location", "")
    availability = request.GET.get("availability", "")
    q = request.GET.get("q", "")
    if blood_group: donors = donors.filter(blood_group=blood_group)
    if location: donors = donors.filter(location__icontains=location)
    if availability: donors = donors.filter(availability=availability)
    if q: donors = donors.filter(Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q) | Q(location__icontains=q))
    return render(request, "core/donor_list.html", {"donors": donors, "blood_groups": [x[0] for x in DonorProfile._meta.get_field("blood_group").choices]})

@login_required
def donor_create(request):
    if hasattr(request.user, "donor_profile"):
        return redirect("donor_edit", pk=request.user.donor_profile.pk)
    form = DonorForm(request.POST or None)
    if form.is_valid():
        donor = form.save(commit=False); donor.user = request.user; donor.save()
        messages.success(request, "Donor profile created.")
        return redirect("donor_detail", donor.pk)
    return render(request, "core/donor_form.html", {"form": form, "title": "Become a Donor"})

def donor_detail(request, pk):
    return render(request, "core/donor_detail.html", {"donor": get_object_or_404(DonorProfile, pk=pk)})

@login_required
def donor_edit(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk, user=request.user)
    form = DonorForm(request.POST or None, instance=donor)
    if form.is_valid():
        form.save(); messages.success(request, "Donor profile updated."); return redirect("donor_detail", pk)
    return render(request, "core/donor_form.html", {"form": form, "title": "Edit Donor Profile"})

@login_required
def donor_delete(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk, user=request.user)
    if request.method == "POST": donor.delete(); messages.success(request, "Donor profile deleted."); return redirect("donor_list")
    return render(request, "core/confirm_delete.html", {"object": donor, "cancel_url": "donor_detail"})

def request_list(request):
    requests = BloodRequest.objects.select_related("requester").all()
    bg, loc, status = request.GET.get("blood_group",""), request.GET.get("location",""), request.GET.get("status","")
    if bg: requests = requests.filter(blood_group=bg)
    if loc: requests = requests.filter(location__icontains=loc)
    if status: requests = requests.filter(status=status)
    return render(request, "core/request_list.html", {"requests": requests, "blood_groups": [x[0] for x in BloodRequest._meta.get_field("blood_group").choices]})

def request_detail(request, pk):
    return render(request, "core/request_detail.html", {"blood_request": get_object_or_404(BloodRequest, pk=pk)})

@login_required
def request_create(request):
    form = BloodRequestForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False); obj.requester = request.user; obj.save()
        messages.success(request, "Blood request created."); return redirect("request_detail", obj.pk)
    return render(request, "core/request_form.html", {"form": form, "title": "Create Blood Request"})

@login_required
def request_edit(request, pk):
    obj = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
    form = BloodRequestForm(request.POST or None, instance=obj)
    if form.is_valid(): form.save(); messages.success(request, "Request updated."); return redirect("request_detail", pk)
    return render(request, "core/request_form.html", {"form": form, "title": "Edit Blood Request"})

@login_required
def request_delete(request, pk):
    obj = get_object_or_404(BloodRequest, pk=pk, requester=request.user)
    if request.method == "POST": obj.delete(); messages.success(request, "Request deleted."); return redirect("my_requests")
    return render(request, "core/confirm_delete.html", {"object": obj, "cancel_url": "request_detail"})

@login_required
def my_requests(request):
    return render(request, "core/my_requests.html", {"requests": BloodRequest.objects.filter(requester=request.user)})
