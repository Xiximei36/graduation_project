import json
from django.views import View
from rest_framework import generics, status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.pagination import PageNumberPagination
from myapps.Orders.models import Orders, OrdersSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.query import QueryHelper
from myapps.utils.model import ModelHelper

# 定义查询字段列表
QUERY_FIELDS = [
    'id',
    'no',
    'num',
    'total',
    'uid',
    'remark',
    'status',
    'create_time',
    'no',
    'realname',
]

# 定义需要模糊查询的字段
FUZZY_FIELDS = [
    'no',
    'realname',
]
# 定义外键字段
FOREIGN_KEYS = [
    'uid',
]

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10       # 每页最多显示的条数
    page_query_param = 'currentPage'   # 查询参数
    page_size_query_param = 'pagesize'
    max_page_size = 100   # 最大页数

#后台分页查询
class selectPageView(generics.GenericAPIView):
    queryset = Orders.objects.order_by('-create_time')
    serializer_class = OrdersSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = OrdersSerializer
    def post(self, request):
        try:
            page = request.data.get("currentPage")
            size = request.data.get("pagesize")
            if not page or not size:
                return ResponseHandler.error(msg='分页参数不能为空')
            try:
                page = int(page)
                size = int(size)
            except ValueError:
                return ResponseHandler.error(msg='分页参数必须是数字')
            request.query_params._mutable = True
            request.query_params['currentPage'] = page
            request.query_params['pagesize'] = size
            request.query_params._mutable = False
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 过滤查询集
            item_queryset = self.get_queryset().filter(q_conditions)
            total = item_queryset.count()
            item_page = self.paginate_queryset(item_queryset)
            if item_page:
                item_serializer = OrdersSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = OrdersSerializer(instance=item_queryset, many=True)
            return ResponseHandler.success_with_page(
                list_data=serializer.data,
                total=total,
                msg='获取成功'
            )
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#后台条件查询
class queryAllView(generics.GenericAPIView):
    queryset = Orders.objects.order_by('-create_time')
    serializer_class = OrdersSerializer
    def post(self, request):
        try:
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 过滤查询集
            item_queryset = self.get_queryset().filter(q_conditions)
            serializer = OrdersSerializer(instance=item_queryset, many=True)
            return ResponseHandler.success(data=serializer.data, msg='获取成功')
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#后端根据ID查询单条
class selectOneView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            if not id:
                return ResponseHandler.error(msg='id不能为空')
            data = Orders.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = OrdersSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#前端分页查询
class frontPageView(generics.GenericAPIView):
    queryset = Orders.objects.order_by('-create_time')
    serializer_class = OrdersSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = OrdersSerializer
    def post(self, request):
        try:
            page = request.data.get("currentPage")
            size = request.data.get("pagesize")
            if not page or not size:
                return ResponseHandler.error(msg='分页参数不能为空')
            try:
                page = int(page)
                size = int(size)
            except ValueError:
                return ResponseHandler.error(msg='分页参数必须是数字')
            request.query_params._mutable = True
            request.query_params['currentPage'] = page
            request.query_params['pagesize'] = size
            request.query_params._mutable = False
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 过滤查询集
            item_queryset = self.get_queryset().filter(q_conditions)
            total = item_queryset.count()
            item_page = self.paginate_queryset(item_queryset)
            if item_page:
                item_serializer = OrdersSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = OrdersSerializer(instance=item_queryset, many=True)
            return ResponseHandler.success_with_page(
                list_data=serializer.data,
                total=total,
                msg='获取成功'
            )
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#前端查询所有
class frontAllView(generics.GenericAPIView):
    queryset = Orders.objects.order_by('-create_time')
    serializer_class = OrdersSerializer
    def post(self, request):
        try:
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 过滤查询集
            item_queryset = self.get_queryset().filter(q_conditions)
            serializer = OrdersSerializer(instance=item_queryset, many=True)
            return ResponseHandler.success(data=serializer.data, msg='获取成功')
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#前端根据ID查询单条
class frontOneView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            if not id:
                return ResponseHandler.error(msg='id不能为空')
            data = Orders.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = OrdersSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#新增
class addView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            serializer_obj = OrdersSerializer(data=dic)
            if not serializer_obj.is_valid():
                return ResponseHandler.error(msg=serializer_obj.errors)
            Orders.objects.create(**serializer_obj.validated_data)
            return ResponseHandler.success(msg='添加成功')
        except Exception as e:
            print("添加出现异常: %s" % e)
            return ResponseHandler.error(msg='添加失败')

#编辑
class editView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body)
            if 'id' not in dic:
                return ResponseHandler.error(msg='id不能为空')
            try:
                id_value = int(dic['id'])
            except (ValueError, TypeError):
                return ResponseHandler.error(msg='id必须是数字')
            obj = Orders.objects.filter(id=id_value).first()
            if not obj:
                return ResponseHandler.error(msg='数据不存在')
            #使用 ModelHelper 更新字段
            ModelHelper.update_model_fields(
                instance=obj,
                data=dic,
                fields=[f for f in QUERY_FIELDS if f != 'id'],  # 排除 id 字段
                foreign_keys=FOREIGN_KEYS  # 使用定义的外键字段列表
            )
            obj.save()  # 保存更新
            return ResponseHandler.success(data=OrdersSerializer(obj).data, msg='更新成功')
        except Exception as e:
            print("更新时出现异常: %s" % e)
            return ResponseHandler.error(msg='更新失败')

#删除
class DelView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            orders = Orders.objects.filter(id=id).first()
            if not orders:
                return ResponseHandler.error(msg='数据不存在')
            orders.delete()
            return ResponseHandler.success(msg='删除成功')
        except Exception as e:
            print("删除时出现异常: %s" % e)
            return ResponseHandler.error(msg='删除失败')

