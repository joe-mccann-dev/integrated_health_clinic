from django.urls import path

from . import views

# register the name space
app_name = "appointments"

urlpatterns = [
    path(
        "", 
        views.IndexView.as_view(), 
        name="index"
    ),
    path(
        "<int:pk>/", 
         views.DetailView.as_view(),
         name="detail"),
    path(
        "modify/",
        views.AddAppointmentView.as_view(),
        name="add"
    ),
    path(
        "modify/<int:pk>/delete",
        views.DeleteAppointmentView.as_view(),
        name="delete"
    ),
    path(
        "notes/<int:pk>",
        views.AppointmentChartView.as_view(),
        name="appointment-chartnote",
    ),
    path(
      "notes/<int:appointment_id>/add",
        views.AddChartNoteView.as_view(),
        name="add-chartnote"
    ),
]
