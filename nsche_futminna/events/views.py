from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import csv
from django.shortcuts import render
from .models import Event
from .models import Event, EventRegistration
from accounts.models import StudentProfile
from django.utils import timezone



@login_required
def events_list(request):
    q = request.GET.get('q', '').strip()
    events = Event.objects.all().order_by('date')
    context = {'events': events}

    if request.user.is_staff and q:
        # search registrations by username or event title
        regs = EventRegistration.objects.filter(student__user__username__icontains=q) | EventRegistration.objects.filter(event__title__icontains=q)
        context.update({'registrations_search_results': regs, 'search_query': q})
    return render(request, 'events/events_list.html', context)



@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    student = request.user.studentprofile

    if request.method == 'POST':
        # Register only if not already registered
        if not EventRegistration.objects.filter(student=student, event=event).exists():
            EventRegistration.objects.create(student=student, event=event)
            messages.success(request, f"Successfully registered for {event.title}!")
        else:
            messages.info(request, f"You are already registered for {event.title}.")

    # After POST, render the events list directly
    events = Event.objects.all()
    registered_event_ids = EventRegistration.objects.filter(student=student).values_list('event_id', flat=True)
    return render(request, 'events/events_list.html', {
        'events': events,
        'registered_event_ids': registered_event_ids
    })


from django.contrib import messages

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Event, EventRegistration

@login_required
def register_event_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data.get('event_id')
        event = Event.objects.get(id=event_id)
        student = request.user.studentprofile

        if EventRegistration.objects.filter(student=student, event=event).exists():
            return JsonResponse({'status': 'error', 'message': 'Already registered.'})

        EventRegistration.objects.create(student=student, event=event)
        return JsonResponse({'status': 'ok', 'message': 'Registered successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


@staff_member_required
def export_registrations_csv(request):
    qs = EventRegistration.objects.select_related('student__user', 'event').all().order_by('registered_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
    writer = csv.writer(response)
    writer.writerow(['id','student_username','student_fullname','event_title','registered_at'])
    for r in qs:
        full = f"{r.student.user.first_name} {r.student.user.last_name}".strip()
        writer.writerow([r.id, r.student.user.username, full, r.event.title, r.registered_at])
    return response



# single list view for public (anonymous) users
# def public_events(request):
#     events = Event.objects.all().order_by('date')
#     return render(request, 'events/public_events.html', {'events': events})


from django.utils import timezone
from django.shortcuts import render
from .models import Event


def public_events(request):
    now = timezone.now()  # current datetime with timezone

    # Upcoming = today + future
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')

    # Past = strictly before now
    past_events = Event.objects.filter(date__lt=now).order_by('-date')

    return render(request, "events/public_events.html", {
        "upcoming_events": upcoming_events,
        "past_events": past_events,
    })





@login_required
def student_events(request):
    student = request.user.studentprofile
    events = Event.objects.all().order_by('date')

    registered_event_ids = list(
        EventRegistration.objects.filter(student=student).values_list('event_id', flat=True)
    )

    return render(request, 'events/student_events.html', {
        'events': events,
        'registered_event_ids': registered_event_ids
    })

# @login_required
# def student_resources(request):

#     student = request.user.studentprofile
#     return render(request, 'events/student_resources.html', {'student': student})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Resource

@login_required
def student_resources(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'events/student_resources.html', {'resources': resources})
