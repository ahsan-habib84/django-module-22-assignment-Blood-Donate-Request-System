from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("donors/", views.donor_list, name="donor_list"),
    path("donors/create/", views.donor_create, name="donor_create"),
    path("donors/<int:pk>/", views.donor_detail, name="donor_detail"),
    path("donors/<int:pk>/edit/", views.donor_edit, name="donor_edit"),
    path("donors/<int:pk>/delete/", views.donor_delete, name="donor_delete"),
    path("requests/", views.request_list, name="request_list"),
    path("requests/create/", views.request_create, name="request_create"),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),
    path("requests/<int:pk>/edit/", views.request_edit, name="request_edit"),
    path("requests/<int:pk>/delete/", views.request_delete, name="request_delete"),
    path("my-requests/", views.my_requests, name="my_requests"),
]
