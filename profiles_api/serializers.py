from django.contrib.auth import get_user_model
from rest_framework import serializers
from profiles_api import models
from profiles_api.models import TodayNote


class TodayNoteSerializer(serializers.ModelSerializer):
    """serializes the today note data"""

    class Meta:
        model = models.TodayNote
        fields = ('id', 'user_profile', 'written_data', 'created_on','emotions')
        extra_kwargs = {'user_profile': {'read_only': True},
                        'id': {'read_only': True}}

    # def create(self, validated_data):
    #     note = validated_data.get('created_on')
    #     if note is not None:
    #         note.written_data = validated_data.get('data')
    #         note.save()
    #     else:
    #         note_data = TodayNote.objects.create(**validated_data)
    #         return note_data


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes the user profile data"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        """Create a new user with encrypted passwond and return it"""
        return get_user_model().objects.create_user(**validated_data)
