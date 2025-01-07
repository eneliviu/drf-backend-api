from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serializer for the current user, extending the UserDetailsSerializer.
    This serializer adds additional read-only fields for the user's profile ID,
    profile image URL, and trip image URL.
    Attributes:
        profile_id (serializers.ReadOnlyField): The ID of the user's profile.
        profile_image (serializers.ReadOnlyField): URL for user profile image.
        image (serializers.ReadOnlyField): The URL of the user's trip image.
    Meta:
        fields (tuple): The fields to be included in the serialization:
                        fields from UserDetailsSerializer.Meta.fields
                        along with 'profile_id', 'profile_image', and 'image'.
    """

    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    image = serializers.ReadOnlyField(source='trip.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image', 'image'
        )
