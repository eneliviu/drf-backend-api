from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    This serializer handles the serialization and deserialization
        of Like model instances.
    It includes fields for the ID, creation timestamp, owner (read-only),
        and the associated trip.
    Additionally, it handles the creation of Like instances, raising a
        validation error if a duplicate like is detected.

    Attributes:
        owner (serializers.ReadOnlyField): username of the like's owner.
    Meta:
        model (Like): The model that this serializer is for.
        fields (list): The fields to be included for serialization.
    Methods:
        create(validated_data):
            Creates a new Like instance, raising a validation error if
                a duplicate like is detected.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Like
        fields = [
            'id', 'created_at', 'owner', 'image'
        ]
        read_only_fields = ['owner', 'created_at']

    def create(self, validated_data):
        image = validated_data.get('image')
        if not image:
            raise serializers.ValidationError(
                {'image': 'This field is required.'}
            )
        try:
            return super().create(validated_data)
        except IntegrityError as err:
            raise serializers.ValidationError(
                {'detail': 'You have already liked this image.'}
            ) from err
