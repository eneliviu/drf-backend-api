from rest_framework import serializers
from .models import Profile
# from followers.models import Follower
from cloudinary.utils import cloudinary_url


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    This serializer handles the serialization and deserialization of Profile
    instances, including custom fields and methods for additional data.

    Fields:
        owner (ReadOnlyField): The username of the profile owner.
        is_owner (SerializerMethodField): Indicates if the current user is
            the owner of the profile.
        following_id (SerializerMethodField): The ID of the following
            relationship between the current user and the profile owner.
        posts_count (ReadOnlyField): The number of posts associated
            with the profile.
        followers_count (ReadOnlyField): The number of followers
            the profile has.
        following_count (ReadOnlyField): The number of profiles the profile
            owner is following.
        image (ImageField): The image associated with the profile.

    Methods:
        get_following_id(obj): Retrieve the ID of the following relationship
            between the authenticated user and the profile owner.
        get_image(obj): Retrieve the URL of the image associated
            with the profile.
        get_is_following(obj): Check if the authenticated user is
            following the profile.
        get_is_owner(obj): Determine if the current user is the owner
            of the profile.
    Meta:
        fields (list): Fields to be included in the serialization.
        read_only_fields (list): Read-only fields that are not modified
            during serialization.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    # following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    image = serializers.ImageField()

    # def get_following_id(self, obj):
    #     """
    #     Retrieve the ID of the following relationship between the
    #     authenticated user and the owner of the given object.
    #     Args:
    #         obj: The object whose owner's following relationship
    #             is to be checked.
    #     Returns:
    #         int or None: The ID of the following relationship if it exists,
    #             otherwise None.
    #     """
    #     user = self.context['request'].user

    #     if user.is_authenticated:
    #         following = Follower.objects.filter(
    #             owner=user,
    #             followed=obj.owner
    #         ).first()
    #         return following.id if following else None
    #     return None

    def get_image(self, obj):
        """
        Retrieve the URL of the image associated with the given object.
        Args:
            obj: The object containing the image.
        Returns:
            str: The URL of the image if it exists, otherwise None.
        """
        if obj.image:
            return cloudinary_url(obj.image.name)[0]
        return None

    # def get_is_following(self, obj):
    #     """
    #     Check if the authenticated user is following the given profile.
    #     Args:
    #         obj: The profile object to check against.
    #     Returns:
    #         bool: True if the authenticated user is following the profile,
    #                 False otherwise.
    #     """
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         return obj.followed_by.filter(id=request.user.profile.id).exists()
    #     return False

    def get_is_owner(self, obj):
        """
        Determine if the current user is the owner of the given object.
        Args:
            obj: The object to check ownership against.
        Returns:
            bool: True if the current user is authenticated and is the owner
                    of the object, False otherwise.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.owner == request.user
        return False

    class Meta:
        """
        Meta class for the Profile serializer.
        Attributes:
            model (Profile): The model that is being serialized.
            fields (list): Dields to be included in the serialization.
            read_only_fields (list): Read-only fields that are not modified
                                        during serialization.
        """

        model = Profile
        # fields = [
        #     'id', 'owner', 'is_owner', 'created_at', 'updated_at', 'name',
        #     'alias', 'content', 'image',  'following_id', 'posts_count',
        #     'followers_count', 'following_count',
        # ]
        fields = '__all__'

        read_only_fields = ['owner', 'created_at', 'updated_at']
