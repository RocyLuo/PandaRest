from rest_framework import serializers
from models import *


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('key', 'value')


class CatalogSerializer(serializers.ModelSerializer):
    variables = VariableSerializer(many=True, required=False)

    class Meta:
        model = Catalog
        fields = '__all__'
        #fields = ('id', 'parent', 'name', 'desc', 'status', 'type', 'repeat', 'create_time', 'priority')

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.repeat = validated_data.get('repeat', instance.repeat)
        instance.priority = validated_data.get('body', instance.priority)

        variables_data = validated_data.pop('variables')
        Variable.objects.filter(catalog=instance).delete()

        for variable_data in variables_data:
            Variable.objects.create(catalog=instance, **variable_data)

        instance.save()
        return instance


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


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    parameters = ParameterSerializer(many=True,required=False)
    headers = HeaderSerializer(many=True,required=False)
    extractors = ExtractorSerializer(many=True,required=False)

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

        Parameter.objects.filter(requestOperation=instance).delete()
        Header.objects.filter(requestOperation=instance).delete()
        Extractor.objects.filter(requestOperation=instance).delete()

        for parameter_data in parameters_data:
            Parameter.objects.create(requestOperation=instance, **parameter_data)

        for header_data in headers_data:
            Header.objects.create(requestOperation=instance, **header_data)

        for extractor_data in extractors_data:
            Extractor.objects.create(requestOperation=instance, **extractor_data)

        instance.save()
        return instance


