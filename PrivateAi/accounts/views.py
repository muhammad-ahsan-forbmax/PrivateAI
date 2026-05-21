# from django.conf import settings
from rest_framework import status
from django.db.transaction import atomic
from django.db.utils import IntegrityError
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, GenericAPIView

from .utils import get_otp, redis_client
from .serializers import RegisterSerializer, NewPasswordSerializer, ForgetPasswordSerializer


User = get_user_model()


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data.get('email')
        username = data.get('username')

        try:
            with atomic():
                user = User.objects.create(username=username, email=email)
                user.is_active = False
                user.save()

        except IntegrityError as e:
            return Response(data={'message': e.__str__()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_otp()
        redis_client.setex(name=f'otp:{username}', time=300, value=otp)
        print(otp)

        return Response(data={'message': 'User created'}, status=status.HTTP_201_CREATED)

class ForgetPassword(GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get('email')
        username = data.get('username')

        if email and username:
            user = User.objects.filter(email=email, username=username).first()
        elif email:
            user = User.objects.filter(email=email).first()
        elif username:
            user = User.objects.filter(username=username).first()
        else:
            user = None

        if not user:
            return Response(data={'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        otp = get_otp()
        redis_client.setex(name=f'otp:{user.username}', time=300, value=otp)
        print(otp)

        return Response(data={'message': 'otp sent for password reset'}, status=status.HTTP_200_OK)

class NewPasswordView(CreateAPIView):
    serializer_class = NewPasswordSerializer

    def create(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)

        data = data.validated_data
        otp = data.get('otp')
        username = data.get('username')
        password = data.get('newpassword')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not (real_otp := redis_client.get(f'otp:{username}')):
            return Response(data={'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if str(real_otp) != str(otp):
            return Response(data={'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(raw_password=password)
        user.is_active = True
        user.save()

        redis_client.delete(f'otp:{username}')

        return Response(data={'message': 'Password created/reset'}, status=status.HTTP_200_OK)
