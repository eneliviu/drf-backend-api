import os
from django.core.exceptions import ValidationError
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
from cloudinary import CloudinaryResource


def get_coordinates(location, attempt=1, max_attempts=5):
    '''
    Geocodes an address with retry on timeout.
    GeoPy documentation:
    https://geopy.readthedocs.io/en/latest/#geopy.exc.GeocoderTimedOut

    Parameters:
        location (str): The location to geocode.
        attempts (int, optional): Current retry attempt. Default is 1.
        max_attempts (int, optional): Maximum retry attempts. Default is 5.

    Returns:
        tuple: Geocoded location data (Latitude and Longitude).

    Raises:
        GeocoderTimedOut: If the max number of attempts is exceeded.
    '''
    geocoder = geocoders.Nominatim(user_agent='trip')
    try:
        get_location = geocoder.geocode(
            location,
            exactly_one=True,
            language='en'
        )

        if get_location:
            return get_location.latitude, get_location.longitude
        return 'location-error'
    except GeocoderTimedOut:
        if attempt < max_attempts:
            return get_coordinates(location,
                                   attempt=attempt+1,
                                   max_attempts=max_attempts)
        raise GeocoderTimedOut("Max attempts exceeded") from None


def validate_image(image):
    """
    Validate the uploaded image file.
    This function checks the file extension of the uploaded image to ensure
    that it is one of the allowed types: .jpg, .jpeg, .png, .gif, .webp.
    If the file extension is not supported, a ValidationError is raised.
    Args:
        image (File): The uploaded image file.
    Raises:
        ValidationError: If the file extension is not supported.
    """
    if not image:
        raise ValidationError("No image provided.")

    valid_extensions = [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".tif", ".tiff"
    ]
    file_extension = None

    try:
        if isinstance(image, CloudinaryResource):
            file_extension = os.path.splitext(image.public_id)[1].lower()
        elif hasattr(image, 'name'):
            file_extension = os.path.splitext(image.name)[1].lower()
        else:
            file_extension = os.path.splitext(str(image))[1].lower()

        if file_extension not in valid_extensions:
            raise ValidationError("Unsupported file extension.")

    except Exception as e:
        raise ValidationError(
            f"Error validating file extension: {str(e)}"
            ) from e

    try:
        if image.size > 1024 * 1024 * 2:  # 2MB size limit
            raise ValidationError("Image size larger than 2MB!")
        if image.image.width > 4096 or image.image.height > 4096:
            raise ValidationError("Image dimensions larger than 4096px!")
    except Exception as e:
        raise ValidationError(
            f"Error validating image properties: {str(e)}"
            ) from e

    return image
