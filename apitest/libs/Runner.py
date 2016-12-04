from ..models import *
from ..config import *
from Request import Request
from Database import Database
import time

#
# class Runner:
#
#     def __init__(self):
#         pass
#
#     def run(self, catalog_id):
#         task_id = "%d" % (time.time() * 1000)
#         cases = self.get_catalog_cases(catalog_id)
#         print str(cases)
#         case_list = self.get_case_list(cases)
#         print str(case_list)
#         for case in case_list:
#             skip_flag = False
#             variables = self.get_case_variables(case['case_id'])
#             catalog_names = self.get_case_parent_names(case['case_id'])
#             for operation in case['operations']:
#                 operation_type = operation['type']
#                 operation_id = operation['id']
#                 operation_log = OperationLog()
#                 operation_log.task_id = task_id
#                 operation_log.type = operation_type
#                 operation_log.case_name = catalog_names[0]
#                 operation_log.module_name = catalog_names[1]
#                 operation_log.project_name = catalog_names[2]
#
#                 if operation_type == 'db':
#                     db_operation = DBOperation.objects.get(pk=operation_id)
#                     db = Database()
#                     db.excute(db_operation.sql)
#                 if operation_type == 'request':
#                     req_operation = RequestOperation.objects.get(pk=operation_id)
#                     request = Request(req_operation.header,req_operation.method,req_operation.url,req_operation.params,req_operation.body,variables,status=req_operation.expect_status,code=req_operation.test_code)
#                     result = request.request(skip_flag)
#                     print result
#                     operation_log.operation_info = result["operation_info"]
#                     operation_log.operation_result = result["operation_result"]
#                     operation_log.assert_result = result["assert_result"]
#                     operation_log.assert_info = result["assert_info"]
#                     operation_log.save()
#                     if req_operation.skip == 1 and not result["assert_result"] == "Pass":
#                         skip_flag = True
#
#     def get_case_parent_names(self, case_id):
#         """
#         :param case_id:
#         :return:[case_name,module_name,project_name]
#         """
#         result = []
#         catalog = Catalog.objects.get(pk=case_id)
#
#         def recur_parents(catalog):
#             result.append(catalog.name)
#             if not catalog.parent_id is None or catalog.parent_id == -1:
#                 parent = Catalog.objects.get(pk=catalog.parent.id)
#                 recur_parents(parent)
#
#         recur_parents(catalog)
#         return result
#
#     def get_catalog_cases(self, catalog_id):
#         """
#         :param catalog_id:
#         :return: [case_id1, case_id2]
#         """
#         result = []
#         catalog = Catalog.objects.get(pk=catalog_id)
#
#         def recur_sub_catalog(catalog):
#             if catalog.type == 'Case':
#                 result.append(catalog)
#
#             children = Catalog.objects.filter(parent_id=catalog.id).exclude(type='RequestTemplate').order_by('priority')
#             if len(children) != 0:
#                 for child in children:
#                     recur_sub_catalog(child)
#
#         recur_sub_catalog(catalog)
#         return result
#
#     def get_case_variables(self, case_id):
#         """
#         :param catalog_id:
#         :return: [ {'key1':value1,'key2':value2,...},{}.... ]  the first variables have the highest priority
#         """
#         result = []
#         catalog = Catalog.objects.get(pk=case_id)
#
#         def recur_parents(catalog):
#             vars = Variable.objects.filter(catalog_id=catalog.id)
#             var_dict = {}
#             for var in vars:
#                 var_dict[var.key] = var.value
#             result.append(var_dict)
#             if not catalog.parent_id is None or catalog.parent_id == -1:
#                 parent = Catalog.objects.get(pk=catalog.parent.id)
#                 recur_parents(parent)
#
#         recur_parents(catalog)
#         return result
#
#     def get_case_operations(self, case_id):
#         result = []
#         result.extend(RequestOperation.objects.filter(catalog__id=case_id))
#         result.extend(DBOperation.objects.filter(catalog__id=case_id))
#         return result
#
#     def get_case_chunks(self, case_id):
#         return CatalogHasChunk.objects.filter(catalog__id=case_id)
#
#     def get_chunk_operations(self, chunk_id):
#         result = []
#         result.extend(RequestOperation.objects.filter(chunk__id=chunk_id))
#         result.extend(DBOperation.objects.filter(chunk__id=chunk_id))
#         return result
#
#     def get_case_operation_list(self, case_id):
#         """
#         :param case_id:
#         :return: {
#                      'case_id':1234
#                      'operations': [{type:'db',id: db_operation_id},{type:'request',id:request_operation_id,...]
#                      }
#         """
#         result = {}
#         result['case_id'] = case_id
#         operations = []
#         mess = []
#         mess.extend(self.get_case_operations(case_id))
#         mess.extend(self.get_case_chunks(case_id))
#         # might spend a lot of time
#         mess = sorted(mess, key=lambda model: model.priority)
#
#         for model in mess:
#             if isinstance(model, CatalogHasChunk):
#                 chunk_operations = self.get_chunk_operations(model.chunk.id)
#                 chunk_operations = sorted(chunk_operations, key=lambda model: model.priority)
#                 for chunk_operation in chunk_operations:
#                     if isinstance(chunk_operation, RequestOperation):
#                         operations.append({'type': operation_name['request'], 'id': chunk_operation.id})
#                     if isinstance(chunk_operation, DBOperation):
#                         operations.append({'type': operation_name['db'], 'id': chunk_operation.id})
#             if isinstance(model,RequestOperation):
#                 operations.append({'type': operation_name['request'], 'id': model.id})
#             if isinstance(model,DBOperation):
#                 operations.append({'type': operation_name['db'], 'id': model.id})
#         result['operations'] = operations
#         return result
#
#
#     def get_case_list(self, cases):
#         """
#         :param: [case_id1, case_id2,...]
#         :return: [
#                    { 'case_id':1234
#                      'operations': [{type:'db',id: db_operation_id},{type:'request',id:request_operation_id,...]
#                      },
#                   { 'case_id':1235
#                      'operations': [{type:'db',id: db_operation_id},{type:'request',id:request_operation_id,...]
#                      }
#                 ]
#         """
#         cases_list = []
#         for case in cases:
#             cases_list.append(self.get_case_operation_list(case.id))
#
#         return cases_list








