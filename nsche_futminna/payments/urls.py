# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('select_dues/', views.select_dues, name='select_dues'),
    path("verify/<str:reference>/", views.verify_payment, name="verify_payment"),
    path('receipt/<int:payment_id>/', views.generate_pdf_receipt, name='generate_receipt'),
    # path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
    path('download-receipt/<str:reference>/', views.download_receipt, name='download_receipt'),
    path('paystack/<str:reference>/', views.paystack_payment, name='paystack_payment'),

]


