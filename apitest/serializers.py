from rest_framework import serializers
from models import Catalog


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id', 'name', 'desc', 'status', 'parent_id', 'create_time', 'priority', 'type')

