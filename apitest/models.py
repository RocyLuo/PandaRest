from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils.timezone import now

class Catalog(models.Model):

    TYPE_CHOICES = (
        ("Project", 'Project'),
        ("Module", 'Module'),
        ("Template", 'Template'),
        ("Case", 'Case'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=-1,blank=True, null=True)
    name = models.CharField(max_length=50)
    desc = models.TextField()
    status = models.SmallIntegerField(default=0)
    priority = models.SmallIntegerField(default=1)
    type = models.CharField(max_length=50,choices=TYPE_CHOICES)
    create_time = models.DateTimeField(auto_now=True)
    repeat = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return 'id:' + str(self.id) + ' name:' + self.name + ' priority:' + str(self.priority) + 'type:'+self.type


class Variable(models.Model):

    catalog = models.ForeignKey(Catalog, related_name='variables',blank=True, null=True)
    data_type = models.CharField(max_length=10, default='str')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key + ":" + self.value


class Function(models.Model):

    catalog = models.ForeignKey(Catalog)
    name = models.CharField(max_length=50)
    desc = models.TextField()
    code = models.TextField()

    def __str__(self):
        return self.desc + ":" + self.code


class RequestOperation(models.Model):

    METHOD_CHOICES = (
        ("get", 'get'),
        ("post", 'post'),
        ("put", 'put'),
        ("delete", 'delete'),
    )
    catalog = models.ForeignKey(Catalog, blank=True, null=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(default="")
    is_template = models.SmallIntegerField(default=0)
    method = models.CharField(max_length=10,choices=METHOD_CHOICES,default='get')
    url = models.CharField(max_length=300,blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    expect_status =  models.SmallIntegerField(default=200,blank=True, null=True)
    test_code = models.TextField(blank=True, null=True)
    expected_body = models.TextField(blank=True, null=True)
    priority = models.SmallIntegerField(default=1)
    skip_next = models.SmallIntegerField(default=1)
    wait_timeout = models.SmallIntegerField(default=0)
    wait_period = models.SmallIntegerField(default=0)
    drive_data = models.TextField(default="",blank=True, null=True)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    requestOperation = models.ForeignKey(RequestOperation,related_name='parameters', blank=True, null=True)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key + ":" + self.value


class Header(models.Model):
    requestOperation = models.ForeignKey(RequestOperation,related_name='headers', blank=True, null=True)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.key + ":" + self.value


class Extractor(models.Model):
    requestOperation = models.ForeignKey(RequestOperation,related_name='extractors', blank=True, null=True)
    variable_name = models.CharField(max_length=50)
    data_type = models.CharField(max_length=10, default='str')
    level = models.CharField(max_length=50, default='temp')
    path = models.CharField(max_length=500)

    def __str__(self):
        return self.variable_name + ":" + self.path


class DBOperation(models.Model):
    catalog = models.ForeignKey(Catalog, blank=True, null=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(default="")
    sql = models.TextField()
    priority = models.SmallIntegerField(default=1)
    skip = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Report(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    project_id = models.IntegerField()
    project_name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='running')
    case_total = models.SmallIntegerField(default=0, blank=True, null=True)
    case_pass = models.SmallIntegerField(default=0, blank=True, null=True)
    case_fail = models.SmallIntegerField(default=0, blank=True, null=True)
    case_error = models.SmallIntegerField(default=0, blank=True, null=True)
    case_skip = models.SmallIntegerField(default=0, blank=True, null=True)


class OperationLog(models.Model):

    RESULT_CHOICES = (
        ("Pass", 'Pass'),
        ("Fail", 'Fail'),
        ("Error", 'Error'),
        ("Skip", 'Skip'),
    )
    report = models.ForeignKey(Report)
    create_time = models.DateTimeField(auto_now=True)
    module_name = models.CharField(max_length=50)
    case_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50,default='default')
    type = models.CharField(max_length=50)
    operation_info = models.TextField()
    operation_result = models.TextField(blank=True, null=True)
    assert_result = models.CharField(max_length=6, choices=RESULT_CHOICES)
    assert_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.report.start_time)+':'+self.module_name+':'+self.case_name+' type:'+self.type+" |"+self.assert_result+'|'+self.assert_info

