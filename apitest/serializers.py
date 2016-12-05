from rest_framework import serializers
from models import Catalog, Variable


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id', 'parent_id', 'name', 'desc', 'status', 'type', 'repeat', 'create_time', 'priority')

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('id', 'catalog_id', 'key', 'value')