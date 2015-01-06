from rest_framework.serializers import ModelSerializer
from .models import TableType, Table
from registration.serializers import RegistrationSerializer


class TableTypeSerializer(ModelSerializer):
    class Meta:
        model = TableType
        fields = ("id", "name", "min_seats", "max_seats")


class TableSerializer(ModelSerializer):
    registration = RegistrationSerializer(required=False)

    class Meta:
        model = Table
        fields = ("id", "table_number", "table_type", "status", "registration")
