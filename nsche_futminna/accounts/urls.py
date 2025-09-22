# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views
# from django.urls import path
# from .views import CustomLoginView, SignupView, CustomLogoutView


# urlpatterns = [
#     path('login/', CustomLoginView.as_view(), name='login'),
#     # path('register/', SignupView.as_view(), name='register'),
#     path('logout/', CustomLogoutView.as_view(), name='logout'),
#     path('register/', views.register, name='register'), 
#     path('login/', views.login_view, name='login'),
#     path('registration/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('profile/', views.profile_view, name='profile'),
#     path('event/<int:event_id>/register/', views.register_event, name='register_event'),
#     path('public/event/<int:event_id>/register/', views.public_event_register, name='public_register_event'),  # public
#     path('profile/complete/', views.profile_complete, name='profile_complete'),

# ]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

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
    path('contact/', views.contact_view, name='contact'),  # New contact form URL
]

