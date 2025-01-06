from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follower model.
    This serializer handles the serialization and deserialization of
    Follower model instances,
    including read-only fields for the owner's username and the followed
        user's username.
    Attributes:
        owner (ReadOnlyField): The username of the owner of the follower
            model instance.
        followed (ReadOnlyField): The username of the followed user.
    Meta:
        model (Follower): The model that is being serialized.
        fields (list): The list of fields to be included in the serialization.
    Methods:
        create(validated_data):
            Creates a new Follower instance. If an IntegrityError occurs,
                raises a ValidationError
            indicating a possible duplicate.
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = [
            'id', 'owner', 'created_at', 'followed', 'followed_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})