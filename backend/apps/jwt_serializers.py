from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that accepts email or username for authentication
    """
    username_field = 'username'  # This will accept the field name as 'username' but can contain email
    
    def validate(self, attrs):
        # Get the username field (which might contain email)
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }
        
        # Use Django's authenticate which will use our custom backend
        user = authenticate(**credentials)
        
        if user is None:
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('No active account found with the given credentials')
        
        # Generate tokens
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return data
