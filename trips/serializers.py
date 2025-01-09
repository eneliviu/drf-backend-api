import os
from rest_framework import serializers
from .models import Trip, Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for handling image uploads and validations.
    Methods:
    --------
    validate_image(value):
        Validates the uploaded image for size, dimensions, and file extension.
    Meta:
    -----
    model: Image
        The model that this serializer is associated with.
    fields: list
        The fields that are included in the serialized output.
    """
    image = serializers.ImageField()

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
            'id',  'owner', 'trip_id', 'image_title',
            'image', 'description', 'shared', 'uploaded_at'
        ]


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trip model.
    Handles the serialization and deserialization of Trip instances,
    including related fields and custom methods for additional data.
    Fields:
        owner (ReadOnlyField): The username of the trip owner.
        is_owner (SerializerMethodField): Indicates if the current user is
                                            the owner of the trip.
        profile_id (ReadOnlyField): The profile ID of the trip owner.
        profile_image (ReadOnlyField): The profile image URL of the trip owner.
        images_count (SerializerMethodField): The count of images associated
                                                with the trip.
        likes_count (SerializerMethodField): The count of likes associated
                                                with the trip.
        images (SerializerMethodField): The images associated with the trip,
                                            filtered by sharing permissions.
    Methods:
        get_images(self, obj): Retrieves the images associated with the trip,
                                filtered by sharing permissions.
        get_is_owner(self, obj): Checks if the current user is the trip owner.
        get_images_count(self, obj): Retrieves the count of images associated
                                        with the trip.
        get_likes_count(self, obj): Retrieves the count of likes associated
                                        with the trip.
        to_representation(self, instance): Customizes the representation of
                                            the trip instance, adding the
                                            images count.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    images_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        """
        Retrieve images associated with the given object.
        If the request user is authenticated and is either the object owner
        or the object is shared, return all images associated with the object.
        Otherwise, return only the images that are marked as shared.
        Args:
            obj: The object for which images are to be retrieved.
        Returns:
            A list of serialized image data.
        """
        request = self.context.get('request')
        if (
            request.user.is_authenticated
                and (obj.owner == request.user or obj.shared)):
            images = obj.images.all()
        else:
            images = obj.images.filter(shared=True)
        return ImageSerializer(images, many=True, context=self.context).data

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    def get_images_count(self, obj):
        return getattr(obj, 'images_count', 0)

    def get_likes_count(self, obj):
        return getattr(obj, 'likes_count', 0)

    def to_representation(self, instance):
        """
        Customize the representation of the instance by adding an
        'images_count' field.
        Args:
            instance (Model): The instance of the model being serialized.
        Returns:
            dict: The serialized representation of the instance with an
                    additional 'images_count' field.
        """
        representation = super().to_representation(instance)
        representation['images_count'] = self.get_images_count(instance)
        return representation

    class Meta:
        model = Trip
        fields = [
            "id", "owner", 'is_owner',  'profile_id', "profile_image",
            "place", "country", "trip_category", "start_date", "end_date",
            "created_at", "updated_at", "trip_status", "shared",
            "images_count", "likes_count", "lat", "lon", 'images'
        ]
