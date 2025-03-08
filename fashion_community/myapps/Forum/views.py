import json
from django.views import View
from rest_framework import generics, status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.pagination import PageNumberPagination
from myapps.Forum.models import Forum, ForumSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.query import QueryHelper
from myapps.utils.model import ModelHelper
from myapps.utils.views import BaseQueryView
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField


# 定义查询字段列表
QUERY_FIELDS = [
    'id',
    'title',
    'content',
    'uid',
    'create_time',
    'title',
    'realname',
]

# 定义需要模糊查询的字段
FUZZY_FIELDS = [
    'title',
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
    queryset = Forum.objects.order_by('-create_time')
    serializer_class = ForumSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = ForumSerializer
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
                item_serializer = ForumSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = ForumSerializer(instance=item_queryset, many=True)
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
    queryset = Forum.objects.order_by('-create_time')
    serializer_class = ForumSerializer
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
            serializer = ForumSerializer(instance=item_queryset, many=True)
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
            data = Forum.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = ForumSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#前端分页查询
class frontPageView(generics.GenericAPIView):
    queryset = Forum.objects.order_by('-create_time')
    serializer_class = ForumSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = ForumSerializer
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
                # 获取分页数据的序列化结果
                item_serializer = ForumSerializer(instance=item_page, many=True)
                serialized_data = item_serializer.data
                
                # 导入Stars模型
                from myapps.Stars.models import Stars
                
                # 为每个帖子添加点赞数量
                for forum_data in serialized_data:
                    if forum_data:
                        # 获取该帖子的点赞数量
                        likes_count = Stars.objects.filter(fid=forum_data['id']).count()
                        # 添加到序列化数据中
                        forum_data['likes'] = likes_count
                
                return ResponseHandler.success_with_page(
                    list_data=serialized_data,
                    total=total,
                    msg='获取成功'
                )
            
            # 如果没有分页数据，处理所有数据
            serializer = ForumSerializer(instance=item_queryset, many=True)
            serialized_data = serializer.data
            
            # 为每个帖子添加点赞数量
            from myapps.Stars.models import Stars
            for forum_data in serialized_data:
                if forum_data:
                    likes_count = Stars.objects.filter(fid=forum_data['id']).count()
                    forum_data['likes'] = likes_count
            
            return ResponseHandler.success_with_page(
                list_data=serialized_data,
                total=total,
                msg='获取成功'
            )
            
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')


#前端分页查询
class frontPageView2(BaseQueryView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    pagination_class = MyPageNumberPagination

    def get_custom_fields(self):
        return {
            'num2': {
                'sql': '''
                    SELECT COUNT(1) 
                    FROM comment 
                    WHERE fid_id = %s
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
            total = queryset.count()
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


#前端查询所有
class frontAllView(generics.GenericAPIView):
    queryset = Forum.objects.order_by('-create_time')
    serializer_class = ForumSerializer
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
            serializer = ForumSerializer(instance=item_queryset, many=True)
            return ResponseHandler.success(data=serializer.data, msg='获取成功')
        except (ParseError, NotFound) as e:
            print("出现如下异常%s" % e)
            return ResponseHandler.error(msg='请求错误')

#前端根据ID查询单条
class frontOneView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            uid = request.GET.get("uid")  # 获取用户ID
            
            if not id:
                return ResponseHandler.error(msg='id不能为空')
            
            # 查询论坛帖子
            forum = Forum.objects.filter(id=id).first()
            if not forum:
                return ResponseHandler.error(msg='数据不存在')
            
            # 序列化数据
            data_serializer = ForumSerializer(instance=forum).data
            
            # 导入Stars模型
            from myapps.Stars.models import Stars
            
            # 获取帖子的总点赞数
            likes_count = Stars.objects.filter(fid=forum.id).count()
            data_serializer['likes'] = likes_count
            
            # 检查当前用户是否点赞
            if uid:
                try:
                    uid = int(uid)
                    is_liked = Stars.objects.filter(
                        fid=forum.id,
                        uid=uid
                    ).exists()
                    data_serializer['liked'] = is_liked
                except (ValueError, TypeError):
                    data_serializer['liked'] = False
            else:
                data_serializer['liked'] = False
            
            return ResponseHandler.success(data=data_serializer, msg='查询成功')
            
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#新增
class addView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            serializer_obj = ForumSerializer(data=dic)
            if not serializer_obj.is_valid():
                return ResponseHandler.error(msg=serializer_obj.errors)
            # 创建基本对象
            insert_data = Forum()
            ModelHelper.update_model_fields(
                instance=insert_data,
                data=dic,
                fields=[f for f in QUERY_FIELDS if f != 'id'],  # 排除 id 字段
                foreign_keys=FOREIGN_KEYS  # 使用定义的外键字段列表
            )
            insert_data.save()
            return ResponseHandler.success(
                data=ForumSerializer(insert_data).data,
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
            obj = Forum.objects.filter(id=id_value).first()
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
            return ResponseHandler.success(data=ForumSerializer(obj).data, msg='更新成功')
        except Exception as e:
            print("更新时出现异常: %s" % e)
            return ResponseHandler.error(msg='更新失败')

#删除
class DelView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            forum = Forum.objects.filter(id=id).first()
            if not forum:
                return ResponseHandler.error(msg='数据不存在')
            forum.delete()
            return ResponseHandler.success(msg='删除成功')
        except Exception as e:
            print("删除时出现异常: %s" % e)
            return ResponseHandler.error(msg='删除失败')

#通用查询方法
def process_goods_query(queryset, request_data):
    try:
        return queryset.order_by('-num2')
    except Exception as e:
        print(f"处理查询时出现异常: {e}")
        return queryset