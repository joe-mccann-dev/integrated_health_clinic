from django.urls import path

from . import views

app_name = "patients"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("modify/", views.AddPatientView.as_view(), name="add"),
  path("modify/<int:pk>/", views.UpdatePatientView.as_view(), name="update"),
  path("modify/<int:pk>/delete", views.DeletePatientView.as_view(), name="delete"),
  path("<int:pk>/notes", views.PatientChartsView.as_view(), name="patient-chartnotes")
]
