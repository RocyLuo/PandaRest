from rest_framework import serializers
from models import *


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ('id', 'parent', 'name', 'desc', 'status', 'type', 'repeat', 'create_time', 'priority')


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('id', 'catalog', 'key', 'value')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestOperation
        fields = '__all__'


