from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from datetime import datetime, timedelta 
from django.contrib.auth import get_user_model
from django.conf import settings 
from .serializers.common import UserSerializer, UserSummarySerializer
from django.shortcuts import get_object_or_404
from countries.models import Country
from rest_framework.permissions import IsAuthenticated
import jwt 


User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        print('USER CREATE', user_to_create)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_202_ACCEPTED)
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied(detail="Invalid Credentials")
        
        if not user_to_login.check_password(password):
            raise PermissionDenied(detail="Invalid Credentials")
        
        dt = datetime.now() + timedelta(days=7)

        token= jwt.encode(
            {'sub': user_to_login.id,
             'name': user_to_login.first_name,
             'userIsAdmin': user_to_login.is_staff,
            'exp': int(dt.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return Response({'token': token, 'message': f'Welcome back {user_to_login.first_name}!!'})

class UserSummaryView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_user(self, request):

        return User.objects.get(pk=request.user.id)
    
    
    def get (self, request):
        user = self.get_user(request)
        user_serialized = UserSummarySerializer(user)
        return Response(user_serialized.data,status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_user(request)
        user.nationality.add(get_object_or_404(Country, name=request.data.get('nationality')))
        user.save()
        return Response({'message': 'Nationality added successfully'}, status=status.HTTP_200_OK)
        
    def delete (self,request,):
        print('Request data:', request.data)
        user = self.get_user(request)
        user.nationality.remove(get_object_or_404(Country, nationality= request.data.get('nationality')))
        user.save()
        return Response({'message': 'Nationality deleted successfully'}, status=status.HTTP_200_OK)
