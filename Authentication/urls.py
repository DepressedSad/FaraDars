from django.urls import path
from .views import signup_form,handle_send_otp,verify_form,handle_verify_otp

urlpatterns=[
    path('signup/',signup_form,name='signup'),
    path('send-otp/',handle_send_otp,name='send-otp'),
    path('verify/',verify_form,name='verify'),
    path('verify-otp/',handle_verify_otp,name='verify-otp'),
]