import base64
import random
import string
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageFunc(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
            return super().to_internal_value(img_data)
        return super().to_internal_value(data)