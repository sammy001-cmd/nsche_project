"""
URL configuration for nsche_futminna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("resources/", TemplateView.as_view(template_name="resources.html"), name="resources"),
    path('events/', TemplateView.as_view(template_name="student_resources.html"), name='student_resources'),
    path("events/", TemplateView.as_view(template_name="public_events.html"), name="public_event"),
    path("events/", TemplateView.as_view(template_name="student_events.html"), name="student"),
    path("events/", include("events.urls")),
    path("contact/", views.contact, name="contact"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    # path("resources/", views.public_resources, name="public_resources"),
    # path("student/resources/", views.student_resources, name="student_resources"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)