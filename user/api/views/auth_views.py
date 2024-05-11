from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_otp.oath import totp

from user.models import AuthUser


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = AuthUser.objects.get(username=request.data.get('username'))

        # Generate OTP token
        device, created = TOTPDevice.objects.get_or_create(user=user)
        device.confirmed = False
        device.save()

        otp_token = totp(device.bin_key)
        print("OTP Token:", otp_token)

        return response


class OTPVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        otp_token = request.data.get('otp_token')
        if not otp_token:
            return Response({"error": "OTP token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the user from the request
        user = request.user

        # Get the OTP device associated with the user
        try:
            device = TOTPDevice.objects.get(user=user)
        except TOTPDevice.DoesNotExist:
            raise AuthenticationFailed('OTP device not found for user')

        # Verify the OTP token
        if not device.verify_token(otp_token):
            raise AuthenticationFailed('Invalid OTP token')
        device.confirmed = True
        device.save()

        return Response({"message": "OTP token verified successfully"})


class CustomLogoutView(APIView):
    """
    Custom logout endpoint to logout user with Simple JWT and unconfirm OTP device.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        # Unconfirmed OTP device if exists
        try:
            device = TOTPDevice.objects.get(user=request.user)
            device.confirmed = False
            device.save()
        except TOTPDevice.DoesNotExist:
            pass

        # Logout user
        logout(request)

        # Blacklist refresh token
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Handle exception
                pass

        return Response({"message": "User logged out successfully."})