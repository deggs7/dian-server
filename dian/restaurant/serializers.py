from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import TableType
from .models import Table
from .models import Restaurant
from registration.serializers import RegistrationSerializer


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "file_key", "create_time", "owner")


class TableTypeSerializer(ModelSerializer):
    class Meta:
        model = TableType
        fields = ("id", "name", "min_seats", "max_seats")


class TableSerializer(ModelSerializer):
    registration = RegistrationSerializer(required=False)
    table_type_info = SerializerMethodField(method_name="get_table_type_info")

    class Meta:
        model = Table
        fields = ("id", "table_number", "table_type", "status", "registration", "table_type_info")

    def get_table_type_info(self, obj):
        table_type = TableType.objects.get(pk=obj.table_type.id)
        return TableTypeSerializer(table_type).data

