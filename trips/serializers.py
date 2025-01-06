from rest_framework import serializers
from .models import Trip, Image


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trip model.
    This serializer converts Trip model instances to JSON format
    and vice versa.
    By default, It includes all fields of the Trip model.
    Attributes:
        Meta (class): Meta options for the serializer.
            model (Trip): The model that is being serialized.
            fields (str): Specifies that all fields of the model should be
                            included in the serialization.
    """

    class Meta:
        model = Trip
        fields = '__all__'


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

    class Meta:
        model = Image
        fields = [
            'id', 'owner', 'trip', 'title', 'image',
            'description', 'shared', 'uploaded_at'
        ]
