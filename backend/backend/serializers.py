from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 
                 'contact_number', 'address', 'filing_status',
                 'preferred_language', 'registration_date', 'is_verified']
        read_only_fields = ['user_id', 'registration_date', 'is_verified']