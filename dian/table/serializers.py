from rest_framework.serializers import ModelSerializer
from table.models import TableType, Table


class TableTypeSerializer(ModelSerializer):
    class Meta:
        model = TableType
        fields = ("id", "name", "min_seats", "max_seats")


class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = ("id", "table_number", "table_type", "status")