from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard & Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),

    # Events
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('public/event/<int:event_id>/register/', views.public_event_register, name='public_register_event'),

    # Contact
    path('contact/', views.contact_view, name='contact'),

    # Password reset flow
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="registration/password_reset_form.html",
            # email_template_name="registration/password_reset_email.txt",   # plain text
            # subject_template_name="registration/password_reset_subject.txt",
            # html_email_template_name="registration/password_reset_email.html",  # HTML design
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    

]


# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views
# from django.contrib.auth import views as auth_views
# from .forms import CustomPasswordResetForm

# urlpatterns = [
#     # Auth
#     path('register/', views.register, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),

#     # Dashboard & Profile
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('profile/', views.profile_view, name='profile'),
#     path('profile/complete/', views.profile_complete, name='profile_complete'),

#     # Events
#     path('event/<int:event_id>/register/', views.register_event, name='register_event'),
#     path('public/event/<int:event_id>/register/', views.public_event_register, name='public_register_event'),
#     path('contact/', views.contact_view, name='contact'),  # New contact form URL
#     path(
#     "password_reset/",
#     auth_views.PasswordResetView.as_view(
#         form_class=CustomPasswordResetForm,
#         template_name="registration/password_reset_form.html",
#         email_template_name="registration/password_reset_email.txt",   # plain text
#         subject_template_name="registration/password_reset_subject.txt",
#         html_email_template_name="registration/password_reset_email.html",  # HTML design
#     ),
#     name="password_reset",
# ),
    
# ]

