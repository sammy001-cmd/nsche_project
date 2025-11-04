from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("profile/", views.admin_profile, name="admin_profile"),
    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),


    # Students
    path("students/", views.student_list, name="student_list"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),

    # Events
    # path("events/", views.admin_event_list, name="admin_event_list"),
    # path("events/create/", views.event_create, name="event_create"),
    # path("events/<int:event_id>/", views.admin_event_detail, name="admin_event_detail"),
    # path("events/<int:event_id>/edit/", views.admin_edit_event, name="admin_edit_event"),
    # path("events/<int:event_id>/delete/", views.event_delete, name="event_delete"),


    # Events
    path("events/", views.admin_events, name="admin_events"),
    path("events/", views.admin_event_list, name="admin_event_list"),
    # path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/edit/", views.admin_edit_event, name="admin_edit_event"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("events/create/", views.event_create, name="event_create"),
    # path("events/<int:event_id>/detail/", views.admin_event_detail, name="admin_event_detail"),
    path('adminpanel/events/<int:pk>/', views.admin_event_detail, name='event_detail'),
    # path("events/edit/<int:event_id>/", views.admin_edit_event, name="admin_edit_event"),
    path("add-event/", views.add_event, name="add_event"),


    # Registrations
    path("registrations/", views.admin_event_registrations, name="admin_event_registrations"),
    # path("registrations/export/excel/", views.export_registrations_excel, name="export_registrations_excel"),
    path("events/<int:pk>/export/csv/", views.export_event_registrations_csv, name="export_event_registrations_csv"),
    # path("events/<int:pk>/export/excel/", views.export_event_registrations_excel, name="export_event_registrations_excel"),


    # Payments (read-only)
    path("payments/", views.admin_payments, name="admin_payments"),
    path("payments/<int:pk>/", views.payment_detail, name="payment_detail"),
    path("payments/export/csv/", views.export_payments_csv, name="export_payments_csv"),

    path("announcements/", views.announcements_list, name="adminpanel_announcements"),
    path("announcements/add/", views.announcement_add, name="adminpanel_announcement_add"),
    path("announcements/<int:pk>/edit/", views.announcement_edit, name="adminpanel_announcement_edit"),
    path("announcements/<int:pk>/delete/", views.announcement_delete, name="adminpanel_announcement_delete"),

]
