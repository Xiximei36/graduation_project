import json
from django.views import View
from rest_framework import generics, status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.pagination import PageNumberPagination
from myapps.Cart.models import Cart, CartSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.query import QueryHelper
from myapps.utils.model import ModelHelper

# 定义查询字段列表
QUERY_FIELDS = [
    'id',
    'gid',
    'num',
    'uid',
    'create_time',
    'goodsName',
    'realname',
]

# 定义需要模糊查询的字段
FUZZY_FIELDS = [
    'goodsName',
    'realname',
]
# 定义外键字段
FOREIGN_KEYS = [
    'gid',
    'uid',
]

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10       # 每页最多显示的条数
    page_query_param = 'currentPage'   # 查询参数
    page_size_query_param = 'pagesize'
    max_page_size = 100   # 最大页数

#后台分页查询
class selectPageView(generics.GenericAPIView):
    queryset = Cart.objects.order_by('-create_time')
    serializer_class = CartSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = CartSerializer
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
                item_serializer = CartSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = CartSerializer(instance=item_queryset, many=True)
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
    queryset = Cart.objects.order_by('-create_time')
    serializer_class = CartSerializer
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
            serializer = CartSerializer(instance=item_queryset, many=True)
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
            data = Cart.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = CartSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#前端分页查询
class frontPageView(generics.GenericAPIView):
    queryset = Cart.objects.order_by('-create_time')
    serializer_class = CartSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = CartSerializer
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
                item_serializer = CartSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = CartSerializer(instance=item_queryset, many=True)
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
    queryset = Cart.objects.order_by('-create_time')
    serializer_class = CartSerializer
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
            serializer = CartSerializer(instance=item_queryset, many=True)
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
            data = Cart.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = CartSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

##新增
class addView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            serializer_obj = CartSerializer(data=dic)
            if not serializer_obj.is_valid():
                return ResponseHandler.error(msg=serializer_obj.errors)

            # 检查商品库存
            from myapps.Goods.models import Goods
            goods = Goods.objects.filter(id=dic.get('gid')).first()
            if not goods:
                return ResponseHandler.error(msg='商品不存在')
            if goods.num < dic.get('num', 0):
                return ResponseHandler.error(msg='库存不足')
            
            # 检查购物车是否已有同一商品
            existing_cart = Cart.objects.filter(
                uid_id=dic.get('uid'),
                gid_id=dic.get('gid')
            ).first()
            
            if existing_cart:
                # 如果已存在，更新数量
                existing_cart.num += dic.get('num', 0)
                existing_cart.save()
            else:
                # 如果不存在，创建新记录
                Cart.objects.create(
                    gid_id=dic.get('gid'),
                    uid_id=dic.get('uid'),
                    num=dic.get('num')
                )
            
            return ResponseHandler.success(msg='操作成功')
            
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
            obj = Cart.objects.filter(id=id_value).first()
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
            return ResponseHandler.success(data=CartSerializer(obj).data, msg='更新成功')
        except Exception as e:
            print("更新时出现异常: %s" % e)
            return ResponseHandler.error(msg='更新失败')

#删除
class DelView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            cart = Cart.objects.filter(id=id).first()
            if not cart:
                return ResponseHandler.error(msg='数据不存在')
            cart.delete()
            return ResponseHandler.success(msg='删除成功')
        except Exception as e:
            print("删除时出现异常: %s" % e)
            return ResponseHandler.error(msg='删除失败')

