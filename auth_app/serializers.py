from rest_framework import serializers
from auth_app.models import  MyUser, OtpModel

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=MyUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=254,write_only=True, required=True)
    class Meta:
        model = MyUser
        fields  = ['username', 'first_name', 'last_name', 'email', 'phone', 'position', 'password', 'password2']

        extra_kwargs = {
            'username':{'required': True},
            'first_name':{'required': True},
            'last_name':{'required': True},
            'email':{'required': True},
            'password2':{'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # return super().validate(attrs)
        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            position = validated_data['position']

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True)
    class Meta:
        model = MyUser
        fields = ['email', 'password']

# class CheckOtpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OtpModel
#         fields = ['id','myuser','otp']
