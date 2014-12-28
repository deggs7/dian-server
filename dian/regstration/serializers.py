from rest_framework.serializers import ModelSerializer, IntegerField, SlugField, PrimaryKeyRelatedField
from .models import Regstration


class RegstrationSerializer(ModelSerializer):
    phone = SlugField(read_only=True)
    table_type = PrimaryKeyRelatedField(read_only=True)
    queue_number = IntegerField(read_only=True)

    class Meta:
        model = Regstration
        fields = ("id", "phone", "table_type", "queue_number", "table")
