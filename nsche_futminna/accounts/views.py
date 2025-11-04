from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, StudentProfileForm
from events.models import Event, EventRegistration
from payments.models import Payment
from .forms import StudentProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import StudentProfile
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import StudentLoginForm
from events.models import Announcement


# -------------------------------
# Register a new student
# -------------------------------

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = StudentProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user temporarily
            user = user_form.save(commit=False)
            raw_password = user_form.cleaned_data["password1"]

            # Save profile temporarily
            profile = profile_form.save(commit=False)

            #  Force username = matric_number (uppercase)
            matric = profile.matric_number.upper()
            user.username = matric
            user.set_password(raw_password)
            user.save()

            # Attach user to profile
            profile.user = user
            profile.save()

            # Auto login
            login(request, user)

            messages.success(request, f"Registration successful 🎉 Welcome {matric}!")
            return redirect("dashboard")
        else:
            # Debugging – print errors in terminal
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)  
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserRegisterForm()
        profile_form = StudentProfileForm()

    return render(request, "registration/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })



# -------------------------------
# Login 
# -------------------------------

def login_view(request):
    """
    Unified login view for both Admins and Students.
    Detects role automatically and redirects accordingly.
    """
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                #  Admin detection
                if user.is_superuser or user.is_staff:
                    messages.success(request, f"Welcome Admin {user.username} 👋")
                    return redirect("admin_dashboard")

                #  Student detection (if profile exists)
                elif hasattr(user, "studentprofile"):
                    messages.success(request, f"Welcome back, {user.studentprofile.full_name} 👋")
                    return redirect("dashboard")

                #  If neither, probably a new or unlinked user
                else:
                    messages.info(request, "Please complete your profile to continue.")
                    return redirect("register")

            else:
                # Invalid credentials
                messages.error(request, "Invalid username or password.")
    else:
        form = StudentLoginForm()

    return render(request, "registration/login.html", {"form": form})





# def login_view(request):
#     if request.method == "POST":
#         form = StudentLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 if user.is_staff:
#                     return redirect('admin_dashboard')
#                 if hasattr(user, "studentprofile"):
#                     return redirect('dashboard')
#                 return redirect('profile_complete')
#             else:
#                 # Invalid credentials
#                 messages.error(request, "Invalid matric number or password.")
#     else:
#         form = StudentLoginForm()

#     return render(request, "registration/login.html", {"form": form})




@login_required
def profile_view(request):
    profile = request.user.studentprofile

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirect back to profile
    else:
        form = StudentProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})






# -------------------------------
# Logout
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------
# Register for a specific event
# -------------------------------
@login_required
def register_event(request, event_id):
    student = request.user.studentprofile
    event = Event.objects.get(id=event_id)

    # Check if already registered
    if not EventRegistration.objects.filter(student=student, event=event).exists():
        EventRegistration.objects.create(student=student, event=event)

    return redirect('dashboard')


def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if not request.user.is_authenticated:
        # Redirect public user to login/signup page
        return redirect('/accounts/login/?next=/accounts/event/{}/register/'.format(event.id))

    # Check if user has a StudentProfile
    try:
        student = request.user.studentprofile
    except:
        # Optional: redirect to login/signup or show a profile form
        return redirect('/accounts/login/?next=/accounts/event/{}/register/'.format(event.id))

    # Register user for the event if not already registered
    registration, created = EventRegistration.objects.get_or_create(
        event=event,
        student=student
    )

    if created:
        # Successfully registered
        return redirect('/events/')  # or wherever
    else:
        # Already registered
        return redirect('/events/')


def public_event_register(request, event_id):
    # --- START: check if user is logged in ---
    if not request.user.is_authenticated:
        messages.info(request, "You need to login or signup first to register for events.")
        return redirect('login')  # <-- redirect to login/signup page
    # --- END: check login ---

    # --- START: forward to main registration view ---
    return register_event(request, event_id)
    # --- END: forward to main registration view ---




@login_required
def profile_complete(request):
    try:
        profile = request.user.studentprofile
        return redirect('home')  # Already has profile
    except:
        if request.method == 'POST':
            form = StudentProfileForm(request.POST)
            if form.is_valid():
                student_profile = form.save(commit=False)
                student_profile.user = request.user
                student_profile.save()
                return redirect('home')
        else:
            form = StudentProfileForm()
    return render(request, 'accounts/profile_complete.html', {'form': form})




# Custom Login View (optional, can just use default)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # your login template

# Signup View
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'  # create this template
    success_url = reverse_lazy('login')  # redirect to login after signup

# Logout View (optional)
# class CustomLogoutView(LogoutView):
#     next_page = reverse_lazy('login')  # redirect after logout

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        # Add an error variable to template
        return self.render_to_response(
            self.get_context_data(form=form, error="Invalid matric number or password.")
        )



def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  #  saves to DB

            # Send mail
            send_mail(
                subject=f"New Contact Message from {contact.name}",
                message=f"From: {contact.name} <{contact.email}>\n\n{contact.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["justinfrank229@gmail.com"],  # official email
            )

            messages.success(request, " Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


from django.shortcuts import get_object_or_404
from django.utils.timezone import now
# @login_required
# def dashboard(request):
#     student = get_object_or_404(StudentProfile, user=request.user)
#     payments = Payment.objects.filter(student=student)

#     upcoming_events = Event.objects.filter(date__gte=now()).order_by('date')[:5]
#     past_events = Event.objects.filter(date__lt=now()).order_by('-date')[:5]

#     print("DEBUG -> Dashboard payments count:", payments.count())
#     for p in payments:
#         print("DEBUG ->", p.reference, p.status, p.amount, p.amount_naira)

#     return render(request, "accounts/dashboard.html", {
#         "student": student,
#         "payments": payments,
#         "upcoming_events": upcoming_events,
#         "past_events": past_events,
#     })


@login_required
def dashboard(request):
    user = request.user

    if user.is_staff or user.is_superuser:
        messages.info(request, "Welcome back, Admin!")
        return redirect('admin_dashboard')  

    try:
        student = StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        messages.warning(request, "No student profile found for this account.")
        return redirect('profile_complete')

    payments = Payment.objects.filter(student=student)
    upcoming_events = Event.objects.filter(date__gte=now()).order_by('date')[:5]
    past_events = Event.objects.filter(date__lt=now()).order_by('-date')[:5]
    announcements = Announcement.objects.all()[:5]

    return render(request, "accounts/dashboard.html", {
        "student": student,
        "payments": payments,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "announcements": announcements,
    })





