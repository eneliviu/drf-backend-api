from rest_framework import serializers
from django.db.models import Count
from django.core.exceptions import ValidationError as DjangoValidationError
from .utils import validate_image as validate_image_file
from .models import Trip, Image
from likes.serializers import LikeSerializer


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model.
    Fields:
        image (ImageField): The uploaded image file.
        owner_name (ReadOnlyField): The username of the image owner, read-only.
    Methods:
        validate_image(value):
            Validates the uploaded image file.
            - Ensures the image size is not larger than 2MB.
            - Ensures the image width is not larger than 4096 pixels.
            - Ensures the image height is not larger than 4096 pixels.
            - Ensures the file extension is one of the supported formats
                        (.jpg, .jpeg, .png, .gif, .webp).
    Meta:
        model (Image): The model that is being serialized.
        fields (list): The list of fields to include in the serialized output.
            - 'id': The ID of the image.
            - 'owner': The owner of the image.
            - 'owner_name': The username of the image owner.
            - 'trip_id': The ID of the associated trip.
            - 'image_title': The title of the image.
            - 'image': The uploaded image file.
            - 'description': The description of the image.
            - 'shared': Whether the image is shared or not.
            - 'uploaded_at': The timestamp when the image was uploaded.
    """
    image = serializers.ImageField()
    likes_count = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.ReadOnlyField(source='owner.username')
    likes = LikeSerializer(many=True, read_only=True)

    def get_likes_count(self, obj):
        '''
        Validate the like counts
        '''
        return getattr(obj, 'likes_count', 0)

    def validate_image(self, value):
        """
        Validate the image field.
        """
        if value:
            try:
                return validate_image_file(value)
            except Exception as e:
                raise serializers.ValidationError(e)
        return value

    def validate_image_title(self, value):
        """
        Validate the image_title field.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Image title must be at least 2 characters."
            )
        return value

    def validate_description(self, value):
        """
        Validate the description field.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "Description must be at least 2 characters."
            )
        return value

    def validate_shared(self, value):
        """
        Validate the shared field.
        """
        if not isinstance(value, bool):
            raise serializers.ValidationError(
                "Shared must be a boolean value."
            )
        return value

    class Meta:
        model = Image
        fields = [
            'id',  'owner', 'owner_name', 'trip_id', 'image_title',
            'image', 'description', 'shared', 'uploaded_at', 'likes_count',
            'likes'
        ]
        read_only_fields = ['owner', 'trip_id', 'uploaded_at', 'id']


class TripSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Trip model.
    This serializer handles the serialization and deserialization of
    Trip instances, including custom fields and validation logic.
    Attributes:
    owner (serializers.ReadOnlyField): The username of the trip owner.
    is_owner (serializers.SerializerMethodField): Indicates if the request
                                                user is the owner of the trip.
    profile_id (serializers.ReadOnlyField): The profile ID of the trip owner.
    profile_image (serializers.ReadOnlyField): The profile image URL of
                                                the trip owner.
    images_count (serializers.SerializerMethodField): The count of images
                                                    associated with the trip.
    likes_count (serializers.SerializerMethodField): The count of likes
                                                    associated with the trip.
    images (serializers.SerializerMethodField): The images associated
                                                    with the trip.
    Methods:
    get_images(obj): Retrieve images associated with the given object.
    get_is_owner(obj): Check if the request user is the owner of the trip.
    get_images_count(obj): Get the count of images associated with the trip.
    get_likes_count(obj): Get the count of likes associated with the trip.
    to_representation(instance): Customize the representation of the instance.
    validate(data): Validate that the start date is before the end date.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    images_count = serializers.SerializerMethodField()
    total_likes_count = serializers.SerializerMethodField()
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
        if request.user.is_authenticated and obj.owner == request.user:
            images = obj.images.all().annotate(
                likes_count=Count('likes')
            ).order_by('-uploaded_at')
        else:
            images = obj.images.filter(shared=True).annotate(
                likes_count=Count('likes')
            ).order_by('-uploaded_at')

        return ImageSerializer(images, many=True, context=self.context).data

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner

    def get_images_count(self, obj):
        return getattr(obj, 'images_count', 0)

    def get_total_likes_count(self, obj):
        return getattr(obj, 'total_likes_count', 0)

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

    def validate(self, data):
        """
        Validate the start and end dates of a trip and ensure they are
        in the correct order.
        Args:
            data (dict): A dictionary containing the trip data to be validated.
        Raises:
            serializers.ValidationError: If the start date is > the end date
                                            or any other validation errors.
        Returns:
            dict: The validated data.
        """

        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                'non_field_errors': ["Start date must be before end date."]
            })
        try:
            instance = Trip(**data)
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                {
                    'non_field_errors': [str(e)]
                }
            )
        return data

    class Meta:
        model = Trip
        fields = [
            "id", "owner", 'is_owner',  'profile_id', "profile_image",
            "place", "country", "trip_category", "start_date", "end_date",
            "created_at", "updated_at", "trip_status", "shared",
            "images_count", "total_likes_count", "lat", "lon", 'images',
            'content', "title"
        ]
