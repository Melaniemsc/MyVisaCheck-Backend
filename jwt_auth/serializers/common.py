from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation 
from django.contrib.auth.hashers import make_password 
from django.core.exceptions import ValidationError
from countries.serializer.common import CountrySerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True) 
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        print('DATA',data)

        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'do not match'})

        try:
            password_validation.validate_password(password=password)
        except ValidationError as err:
            print('VALIDATION ERROR')
            raise ValidationError({ 'password': err.messages })

        data['password'] = make_password(password)

        print('DATA ->', data)
        return data

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation')


class UserSummarySerializer(serializers.ModelSerializer): 
    nationality = CountrySerializer(many=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'nationality')
