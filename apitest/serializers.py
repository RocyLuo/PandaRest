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


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('key', 'value')


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = ('key', 'value')


class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor
        fields = ('variable_name', 'path')


class RequestSerializer(serializers.ModelSerializer):
    parameters = ParameterSerializer(many=True,required=True)
    headers = HeaderSerializer(many=True,required=True)
    extractors = ExtractorSerializer(many=True,required=True)

    class Meta:
        model = RequestOperation
        fields = '__all__'

    def update(self, instance, validated_data):

        instance.url = validated_data.get('url', instance.url)
        instance.expect_status = validated_data.get('expect_status', instance.expect_status)
        instance.method = validated_data.get('method', instance.method)
        instance.body = validated_data.get('body', instance.body)
        instance.test_code = validated_data.get('test_code', instance.test_code)
        instance.expected_body = validated_data.get('expected_body', instance.expected_body)
        instance.wait_timeout = validated_data.get('wait_timeout', instance.wait_timeout)
        instance.wait_period = validated_data.get('wait_period', instance.wait_period)
        instance.drive_data = validated_data.get('drive_data', instance.drive_data)
        instance.skip_next = validated_data.get('skip_next', instance.skip_next)

        parameters_data = validated_data.pop('parameters')
        headers_data = validated_data.pop('headers')
        extractors_data = validated_data.pop('extractors')

        Parameter.objects.filter(RequestOperation=instance).delete()
        Header.objects.filter(RequestOperation=instance).delete()
        Extractor.objects.filter(RequestOperation=instance).delete()

        for parameter_data in parameters_data:
            Parameter.objects.create(RequestOperation=instance, **parameter_data)

        for header_data in headers_data:
            Header.objects.create(RequestOperation=instance, **header_data)

        for extractor_data in extractors_data:
            Extractor.objects.create(RequestOperation=instance, **extractor_data)

        instance.save()
        return instance


