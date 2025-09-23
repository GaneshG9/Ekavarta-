from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, UserVerification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 
                 'user_type', 'is_verified', 'verification_status', 'business_name', 
                 'business_type', 'interested_services', 'city', 'state', 'country']
        read_only_fields = ['id', 'is_verified', 'verification_status']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 
                 'last_name', 'phone_number', 'user_type', 'business_name', 'business_type']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ['verification_type', 'is_verified', 'verified_at', 'document_type']
        read_only_fields = ['is_verified', 'verified_at']