from django.urls import path

from . import views

urlpatterns = [
    path("", views.AppointmentListView.as_view(), name="index"),
]
