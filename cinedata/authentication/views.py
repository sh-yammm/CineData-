from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from .serializers import ProfileSerializer
from .models import OTP
from django.db import transaction
from . utility import sending_sms
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .utility import get_otp

# Create your views here.

class LoginView(APIView):

    http_method_names = ['post']

    def post(self,request,*args,**kwargs):

        username = request.data.get('username')

        password = request.data.get('password')

        user = authenticate(username=username,password=password)

        if user :

            access_token = RefreshToken.for_user(user).access_token

            return Response(data={'access_token': str(access_token)},status=200)
        
        return Response(data={'msg':'invalid credentials'},status=401)
    

class UserRegistration(APIView):

    http_method_names = ['post']

    authentication_classes = [JWTAuthentication]

    permission_classes = [AllowAny]

    serializer_class = ProfileSerializer

    def post(self,request,*args,**kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            with transaction.atomic():

                profile = serializer.save()

                profile.role = 'User'

                email = request.data.get('email')

                password = request.data.get('password')

                profile.set_password(password)

                profile.username = email 

                profile.save()

                otp = '1234'

                otp_obj = OTP.objects.create(user = profile,otp=otp)

                phone_num = f'+91{profile.mobile_num}'

                sending_sms(phone_num,otp)

                return Response(data={'msg':'verify account using otp'},status=200)
        
        return Response(data=serializer.errors,status=400)
    

class OTPVerifyView(APIView):

    http_method_names = ['post']

    authentication_classes = [JWTAuthentication]

    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):

        mobile_num = request.data.get('mobile_num')

        otp = request.data.get('otp')

        otp_obj = OTP.objects.get(user__mobile_num=mobile_num)
        
        time_now = timezone.now()

        otp_time = otp_obj.updated_at

        if time_now-otp_time <= timezone.timedelta(minutes=10):

            if otp == otp_obj.otp:

                otp_obj.user.is_active = True

                otp_obj.user.save()

                return Response(data={'msg':'user verified successfully'},status=200)
            
            return Response(data={'msg':'Invalid otp'},status=400)
        
        return Response(data={'msg':'otp expired'},status=400)

class OTPRegenerateView(APIView):

    def post(self,request,*args,**kwargs):

        mobile_num = request.data.get('mobile_num')

        otp_obj = get_object_or_404(OTP,user__mobile_num=mobile_num)

        otp = get_otp()

        otp_obj.otp = otp

        otp_obj.save()

        phone_num = f'+91{mobile_num}'

        sending_sms(phone_num,otp)

        return Response(data={'msg':'verify account using otp'},status=200)
    