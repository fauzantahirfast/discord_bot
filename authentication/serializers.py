from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserAccountDetails


class DiscordAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountDetails
        fields = '__all__'
        

    def create(self, validated_data):
        object_find = UserAccountDetails.objects.filter(id = validated_data['id'])
        if object_find.exists():
            new_instance = UserAccountDetails.objects.get(id = validated_data['id'])
        else:
            new_instance =  UserAccountDetails.objects.create(**validated_data)
        return new_instance
    
    
class CustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    user_id = serializers.CharField()