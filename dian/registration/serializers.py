from rest_framework.serializers import ModelSerializer, IntegerField, SlugRelatedField
from .models import Registration


class RegistrationSerializer(ModelSerializer):
    queue_number = IntegerField(read_only=True)

    class Meta:
        model = Registration
        fields = ("id", "phone", "table_type", "queue_number", "table", "expire")
