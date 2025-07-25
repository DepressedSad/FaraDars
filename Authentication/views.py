from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import OTP
from .utils import generate_otp,send_otp_email
from .serializers import EmailSerializer,OTPVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

def signup_form(request):
    return render(request,'signup.html')

def verify_form(request):
    return render(request,'verify.html')

def handle_send_otp(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if not email:
            return render(request,'signup.html',{'error':'Email is required!'})
        if not email.endswith('@gmail.com'):
            return render(request,'signup.html',{'error':'Only Gmail is allowed!'})
        otp=generate_otp()
        send_otp_email(email,otp)
        OTP.objects.create(email=email,code=otp)
        request.session['email']=email
        return redirect('verify')
    
def handle_verify_otp(request):
    if request.method=='POST':
        code=request.POST.get('code')
        email=request.session.get('email')
        if not email:
            return redirect('signup')
        try:
            otp=OTP.objects.filter(email=email,code=code,is_verified=False).latest('created_at')
            if otp.is_valid():
                otp.is_verified=True
                otp.save()
                user,created=User.objects.get_or_create(username=email,email=email)
                refresh=RefreshToken.for_user(user)
                request.session['access_token']=str(refresh.access_token)
                request.session['refresh_token']=str(refresh)
                del request.session['email']
                return render(request,'success.html')
            else:
                return render(request,'verify.html',{'error':'The code has expired!'})
        except OTP.DoesNotExist:
            return render(request,'verify.html',{'error':'The code is invalid!'})

class SendOTPView(APIView):
    def post(self,request):
        email=request.POST.get('email') or request.data.get('email')
        if not email:
            return Response({'error':'Email is required.'},status=400)
        if not email.endswith('@gmail.com'):
            return Response({'error':'Only Gmail addresses allowed.'},status=400)
        otp_code=generate_otp()
        send_otp_email(email,otp_code)
        OTP.objects.create(email=email,code=otp_code)
        return Response({'message':'OTP sent successfully.'})
    
class VerifyOTPView(APIView):
    def post(self,request):
        serializer=OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            code=serializer.validated_data['code']
            try:
                otp=OTP.objects.filter(email=email,code=code,is_verified=False).latest('created_at')
                if otp.is_valid():
                    otp.is_verified=True
                    otp.save()
                    user,created=User.objects.get_or_create(username=email,email=email)
                    refresh=RefreshToken.for_user(user)
                    request.session['access_token']=str(refresh.access_token)
                    request.session['refresh_token']=str(refresh)                    
                    return Response({
                        'message':'OTP verified. Login successful.'
                    })
                else:
                    return Response({'error':'OTP expired.'},status=400)
            except OTP.DoesNotExist:
                return Response({'error':'Invalid OTP.'},status=400)
        return Response(serializer.errors,status=400)