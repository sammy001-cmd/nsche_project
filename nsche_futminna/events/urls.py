from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from .views import export_registrations_csv

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('export-registrations-csv/', views.export_registrations_csv, name='export_registrations_csv'),
        # Public view (anonymous visitors)
    path('events/', views.public_events, name='events_list'),
    # Student view (must be logged in)
    path('my-events/', views.student_events, name='student_events'),
    # Register for a specific event
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),

    path("", views.public_events, name="public_events"),
    path("student/", views.student_events, name="student_events"),
    path("student_resources/", views.student_resources, name="student_resources"),
    path('register-event-ajax/', views.register_event_ajax, name='register_event_ajax'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)