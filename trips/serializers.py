import os
from rest_framework import serializers
from .models import Trip, Image
from cloudinary.utils import cloudinary_url


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trip model.
    This serializer converts Trip model instances to JSON format
    and vice versa.
    It includes the following fields:

    Attributes:
        Meta (class): Meta options for the serializer.
            model (Trip): The model that is being serialized.
            fields (str): Specifies that all fields of the model should be
                            included in the serialization.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    images_count = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    def get_images_count(self, obj):
        return getattr(obj, 'images_count', 0)

    # def to_representation(self, instance):
    #     # Adding the annotated field to the representation explicitly
    #     representation = super().to_representation(instance)
    #     representation['images_count'] = self.get_images_count(instance)
    #     return representation

    class Meta:
        model = Trip
        fields = [
            "id", "owner", 'is_owner',  'profile_id', "profile_image",
            "place", "country", "trip_category", "start_date", "end_date",
            "created_at", "updated_at", "trip_status", "shared",
            "images_count", "lat", "lon"
        ]


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model that automatically handles the
    CloudinaryField and convert it to a URL string in the JSON output.
    It includes the following fields:
    - id: The unique identifier for the image.
    - owner: The user who owns the image.
    - trip: The trip associated with the image.
    - title: The title of the image.
    - image: The image file.
    - description: A description of the image.
    - shared: A boolean indicating if the image is shared.
    - uploaded_at: The timestamp when the image was uploaded.
    """

    def validate_image(self, value):
        # value is the uploaded image
        if value.size > 1024 * 1024 * 2:  # 2MB size limit
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:  # max 4096 px width
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )

        file_extension = os.path.splitext(value.name)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.gif', 'webp']:
            raise serializers.ValidationError("Unsupported file extension.")

        return value

    class Meta:
        model = Image
        fields = [
            'id', 'owner', 'trip', 'image_title',
            'image', 'description', 'shared', 'uploaded_at'
        ]
