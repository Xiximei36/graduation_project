import json
from django.views import View
from rest_framework import generics, status, request
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.pagination import PageNumberPagination
from myapps.Goods.models import Goods, GoodsSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.query import QueryHelper
from myapps.utils.model import ModelHelper
from myapps.utils.views import BaseQueryView
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.db.models import Count
from myapps.OrderItem.models import OrderItem

# 定义查询字段列表
QUERY_FIELDS = [
    'id',
    'cid',
    'image',
    'name',
    'remark',
    'money',
    'num',
    'content',
    'status',
    'create_time',
    'name',
    'categoryName',
]

# 定义需要模糊查询的字段
FUZZY_FIELDS = [
    'name',
    'categoryName',
]
# 定义外键字段
FOREIGN_KEYS = [
    'cid',
]

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10       # 每页最多显示的条数
    page_query_param = 'currentPage'   # 查询参数
    page_size_query_param = 'pagesize'
    max_page_size = 100   # 最大页数

#后台分页查询
class selectPageView(BaseQueryView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = MyPageNumberPagination

    def get_custom_fields(self):
        return {
            'sale': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM order_item 
                    WHERE gid_id = %s
                ''',
                'params': lambda obj: [obj.id]
            }
        }

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

            # 获取基础查询集
            queryset = self.get_queryset()

            # 应用基本查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            queryset = queryset.filter(q_conditions)

            # 应用商品特定的查询处理
            queryset = process_goods_query(queryset, request.data)

            # 获取总数
            total = queryset.count()

            # 分页
            page_queryset = self.paginate_queryset(queryset)
            if page_queryset is not None:
                serializer = self.get_serializer(page_queryset, many=True)
                data = serializer.data

                # 为每条记录添加自定义字段
                for item, instance in zip(data, page_queryset):
                    self.process_serializer_data(item, instance)

                return ResponseHandler.success_with_page(
                    list_data=data,
                    total=total,
                    msg='获取成功'
                )

            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # 为每条记录添加自定义字段
            for item, instance in zip(data, queryset):
                self.process_serializer_data(item, instance)

            return ResponseHandler.success_with_page(
                list_data=data,
                total=total,
                msg='获取成功'
            )
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#后台条件查询
class queryAllView(BaseQueryView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get_custom_fields(self):
        return {
            'sale': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM order_item 
                    WHERE gid_id = %s
                ''',
                'params': lambda obj: [obj.id]
            }
        }

    def post(self, request):
        try:
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 获取查询集
            queryset = self.get_queryset().filter(q_conditions)
            
            # 应用商品特定的查询处理
            queryset = process_goods_query(queryset, request.data)
            
            # 序列化数据
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # 为每条记录添加自定义字段
            for item, instance in zip(data, queryset):
                self.process_serializer_data(item, instance)

            return ResponseHandler.success(data=data, msg='获取成功')
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
            data = Goods.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = GoodsSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#前端分页查询
class frontPageView(BaseQueryView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = MyPageNumberPagination

    def get_custom_fields(self):
        return {
            'sale': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM order_item 
                    WHERE gid_id = %s
                ''',
                'params': lambda obj: [obj.id]
            }
        }

    def post(self, request):
        try:
            # 处理分页参数
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

            # 获取基础查询集
            queryset = self.get_queryset()

            # 应用基本查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            queryset = queryset.filter(q_conditions)

            # 应用商品特定的查询处理
            queryset = process_goods_query(queryset, request.data)

            # 获取总数
            total = queryset.count()

            # 分页
            page_queryset = self.paginate_queryset(queryset)
            if page_queryset is not None:
                serializer = self.get_serializer(page_queryset, many=True)
                data = serializer.data

                # 为每条记录添加自定义字段
                for item, instance in zip(data, page_queryset):
                    self.process_serializer_data(item, instance)

                return ResponseHandler.success_with_page(
                    list_data=data,
                    total=total,
                    msg='获取成功'
                )

            # 如果没有分页，处理所有数据
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # 为每条记录添加自定义字段
            for item, instance in zip(data, queryset):
                self.process_serializer_data(item, instance)

            return ResponseHandler.success_with_page(
                list_data=data,
                total=total,
                msg='获取成功'
            )

        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='请求错误')

#前端查询所有
class frontAllView(BaseQueryView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get_custom_fields(self):
        return {
            'sale': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM order_item 
                    WHERE gid_id = %s
                ''',
                'params': lambda obj: [obj.id]
            }
        }

    def post(self, request):
        try:
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            # 获取查询集
            queryset = self.get_queryset().filter(q_conditions)
            
            # 应用商品特定的查询处理
            queryset = process_goods_query(queryset, request.data)
            
            # 序列化数据
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # 为每条记录添加自定义字段
            for item, instance in zip(data, queryset):
                self.process_serializer_data(item, instance)

            return ResponseHandler.success(data=data, msg='获取成功')
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
            
            # 查询商品信息
            goods = Goods.objects.filter(id=id).first()
            if not goods:
                return ResponseHandler.error(msg='数据不存在')
            
            # 序列化商品数据
            data_serializer = GoodsSerializer(instance=goods).data
            
            # 获取商品评价列表
            from myapps.Review.models import Review, ReviewSerializer
            reviews = Review.objects.filter(gid=goods.id).order_by('-create_time')
            
            # 添加评价列表到返回数据中
            data_serializer['reviews'] = ReviewSerializer(reviews, many=True).data
            
            return ResponseHandler.success(data=data_serializer, msg='查询成功')
            
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#新增
class addView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            serializer_obj = GoodsSerializer(data=dic)
            if not serializer_obj.is_valid():
                return ResponseHandler.error(msg=serializer_obj.errors)

            # 创建基本对象
            insert_data = Goods()
            
            # 使用 ModelHelper 更新字段，包括外键
            ModelHelper.update_model_fields(
                instance=insert_data,
                data=dic,
                fields=[f for f in QUERY_FIELDS if f != 'id'],  # 排除 id 字段
                foreign_keys=FOREIGN_KEYS  # 使用定义的外键字段列表
            )
            
            # 保存对象
            insert_data.save()
            
            return ResponseHandler.success(
                data=GoodsSerializer(insert_data).data,
                msg='添加成功'
            )
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
            obj = Goods.objects.filter(id=id_value).first()
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
            return ResponseHandler.success(data=GoodsSerializer(obj).data, msg='更新成功')
        except Exception as e:
            print("更新时出现异常: %s" % e)
            return ResponseHandler.error(msg='更新失败')

#删除
class DelView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            goods = Goods.objects.filter(id=id).first()
            if not goods:
                return ResponseHandler.error(msg='数据不存在')
            goods.delete()
            return ResponseHandler.success(msg='删除成功')
        except Exception as e:
            print("删除时出现异常: %s" % e)
            return ResponseHandler.error(msg='删除失败')

#前端销量排行
class frontBySalesView(BaseQueryView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get_custom_fields(self):
        return {
            'sale': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM order_item 
                    WHERE gid_id = %s
                ''',
                'params': lambda obj: [obj.id]
            }
        }

    def post(self, request):
        try:
            # 获取基础查询集
            queryset = self.get_queryset()
            
            # 构建查询条件
            q_conditions = QueryHelper.build_query_conditions(
                request.data,
                QUERY_FIELDS,
                fuzzy_fields=FUZZY_FIELDS
            )
            
            # 过滤查询集并添加销量统计
            queryset = queryset.filter(q_conditions).annotate(
                sales_count=Count('orderitem')  # 通过反向关联名统计订单项数量
            ).order_by('-sales_count')[:5]  # 按销量降序并取前5条
            
            # 序列化数据
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # 为每条记录添加自定义字段
            for item, instance in zip(data, queryset):
                self.process_serializer_data(item, instance)
                # 添加销量到返回数据
                item['sales_count'] = getattr(instance, 'sales_count', 0)

            return ResponseHandler.success(data=data, msg='获取成功')
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

def process_goods_query(queryset, request_data):
    """
    处理商品查询的通用方法
    包含金额转换、金额范围过滤、排序等功能
    """
    try:
        # 将字符串金额转换为浮点数
        queryset = queryset.annotate(
            money_float=Cast('money', output_field=FloatField())
        )

        # 处理金额范围过滤
        money_type = request_data.get('money1')
        if money_type:
            money_ranges = {
                '1': Q(money_float__lt=100),
                '2': Q(money_float__gte=100) & Q(money_float__lt=300),
                '3': Q(money_float__gte=300) & Q(money_float__lt=500),
                '4': Q(money_float__gte=500) & Q(money_float__lt=1000),
                '5': Q(money_float__gte=1000)
            }
            money_filter = money_ranges.get(str(money_type))
            if money_filter:
                queryset = queryset.filter(money_filter)

        # 处理排序
        sort_by = request_data.get('sortBy')
        if sort_by:
            # 如果是按销量排序，添加销量注解
            if sort_by == '4':
                queryset = queryset.annotate(
                    sales_count=Count('orderitem')
                ).order_by('-sales_count')
            else:
                sort_mappings = {
                    '1': 'name',          # 按名称正序
                    '2': 'money_float',   # 按价格正序
                    '3': '-money_float',  # 按价格倒序
                    '5': '-create_time'   # 按时间倒序
                }
                if sort_by in sort_mappings:
                    queryset = queryset.order_by(sort_mappings[sort_by])

        return queryset
    except Exception as e:
        print(f"处理商品查询时出现异常: {e}")
        return queryset

