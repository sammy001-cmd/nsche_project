# payments/views.py
import uuid
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from accounts.models import StudentProfile
from events.models import Event
from .models import Payment
from .forms import DuesSelectionForm


# 1 Student dashboard with events & payment history
def student_dashboard(request):
    student = request.user.studentprofile
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    past_events = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
    payments = Payment.objects.filter(student=student).order_by('-created_at')

    return render(request, 'dashboard/student_dashboard.html', {
        'student': student,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'payments': payments,
    })


# 2 Dues selection (new or returning student)
def select_dues(request):
    student = request.user.studentprofile

    if request.method == "POST":
        form = DuesSelectionForm(request.POST)
        if form.is_valid():
            student_type = form.cleaned_data['student_type']
            amount = 1500 if student_type == "new" else 1000

            # Create pending payment
            payment = Payment.objects.create(
                student=student,
                amount=amount * 100,  # store in kobo
                reference=str(uuid.uuid4()),
                status="pending",
                description=f"{student_type.capitalize()} Student Dues"
            )
            return redirect("paystack_payment", reference=payment.reference)
    else:
        form = DuesSelectionForm()

    return render(request, "payments/select_dues.html", {"form": form})


# 3 Initialize payment with Paystack
def initiate_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    amount_kobo = payment.amount

    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email,
        "amount": amount_kobo,
        "reference": reference,
        "callback_url": request.build_absolute_uri(f"/payments/verify/{reference}/"),
    }

    response = requests.post(url, json=data, headers=headers)
    res_data = response.json()

    if res_data.get("status"):
        return redirect(res_data["data"]["authorization_url"])
    else:
        messages.error(request, "Payment initialization failed. Try again.")
        return redirect("student_dashboard")


# 4 Verify payment & generate PDF receipt

def verify_payment(request, reference):
    payment = get_object_or_404(Payment, reference=reference)

    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()

    if data['status'] and data['data']['status'] == 'success':
        # Paystack returns amount already in kobo
        amount_in_kobo = data['data']['amount']

        payment.amount = amount_in_kobo   #  stay consistent (always kobo)
        payment.status = "success"
        payment.save()

        return generate_pdf_receipt(payment)
    else:
        payment.status = "failed"
        payment.save()
        return HttpResponse("Payment verification failed. Please try again.", status=400)

# def verify_payment(request, reference):
#     payment = get_object_or_404(Payment, reference=reference)

#     url = f"https://api.paystack.co/transaction/verify/{reference}"
#     headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
#     resp = requests.get(url, headers=headers)
#     data = resp.json()

#     if data['status'] and data['data']['status'] == 'success':
#         # Paystack returns amount in kobo, so divide by 100 to get Naira
#         amount_in_naira = data['data']['amount'] / 100

#         payment.amount = amount_in_naira
#         payment.status = "success"
#         payment.save()
#         return generate_pdf_receipt(payment)
#     else:
#         payment.status = "failed"
#         payment.save()
#         return HttpResponse(
#             "Payment verification failed. Please try again.", status=400
#         )



# 5 Generate PDF receipt (can be reused)
def generate_pdf_receipt(payment):
    template = get_template('payments/receipt.html')
    html = template.render({'payment': payment})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.reference}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response


# 6 Direct download receipt (only successful payments)
def download_receipt(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    if payment.status != "success":
        return HttpResponse("Receipt available only for successful payments.", status=400)
    return generate_pdf_receipt(payment)

# payments/views.py
def paystack_payment(request, reference):
    # Simply call your existing initiate_payment logic
    return initiate_payment(request, reference)
