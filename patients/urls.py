from django.urls import path

from . import views

app_name = "patients"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("modify/", views.AddPatientView.as_view(), name="add"),
  path("modify/<int:pk>/", views.UpdatePatientView.as_view(), name="update"),
  path("modify/<int:pk>/delete", views.DeletePatientView.as_view(), name="delete"),
  path("<int:pk>/notes", views.PatientChartsView.as_view(), name="patient-chartnotes"),
  path("<int:patient_id>/prescription/add", views.AddPatientPrescriptionView.as_view(), name="add-prescription"),
  path("<int:patient_id>/prescription/<int:pk>/delete", views.DeletePatientPrescriptionView.as_view(), name="delete-prescription"),
  path("<int:patient_id>/prescription/<int:pk>/update", views.UpdatePatientPrescriptionView.as_view(), name="update-prescription"),
]
