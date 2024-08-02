from django.urls import path
from . import views

app_name = "practitioners"
urlpatterns = [
    path(
        "",
        views.PractitionerIndexView.as_view(),
        name="index",
    ),
    path(
        "<int:pk>/",
        views.PractitionerDetailView.as_view(),
        name="detail",
    ),
    path(
        "<int:pk>/appointments/",
        views.PractitionerAppointmentsView.as_view(), 
        name = "appointments"
    ),
    path(
        "<int:pk>/chartnotes",
        views.PractitionerChartsView.as_view(),
        name="chartnotes",
    ),
]