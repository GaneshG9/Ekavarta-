from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User, UserProfile, UserVerification
from .serializers import UserSerializer, UserProfileSerializer, UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create auth token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    """
    User login endpoint
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    """
    User logout endpoint
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout successful'})
        except:
            return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(generics.GenericAPIView):
    """
    Account verification endpoint
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Verification token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            verification = UserVerification.objects.get(verification_token=token, is_verified=False)
            verification.is_verified = True
            verification.verified_at = timezone.now()
            verification.save()
            
            user = verification.user
            user.is_verified = True
            user.verification_status = 'verified'
            user.save()
            
            return Response({'message': 'Account verified successfully'})
        except UserVerification.DoesNotExist:
            return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile management
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
