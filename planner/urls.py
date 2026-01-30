from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plan/create/", views.plan_create, name="plan_create"),
    path("plan/<int:plan_id>/", views.plan_detail, name="plan_detail"),
    path("activities/", views.activity_list, name="activity_list"),
    path("activities/create/", views.activity_create, name="activity_create"),
    path(
        "activities/delete/<int:activity_id>/",
        views.activity_delete,
        name="activity_delete",
    ),
    path("session/update/", views.session_update, name="session_update"),
    path("sessions/bulk/", views.sessions_bulk_update, name="sessions_bulk_update"),
]
