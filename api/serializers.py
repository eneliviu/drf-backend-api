from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer


class CurrentUserSerializer(UserDetailsSerializer):
    '''
    Custom user serializer to include profile_id, profile_image and image fields.
    '''
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    image = serializers.ReadOnlyField(source='trip.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image', 'image'
        )
