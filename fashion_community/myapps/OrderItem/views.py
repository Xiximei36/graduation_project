import json
from django.views import View
from rest_framework import generics, status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.pagination import PageNumberPagination
from myapps.OrderItem.models import OrderItem, OrderItemSerializer
from myapps.utils.response import ResponseHandler
from myapps.utils.query import QueryHelper
from myapps.utils.model import ModelHelper

# 定义查询字段列表
QUERY_FIELDS = [
    'id',
    'oid',
    'gid',
    'num',
    'money',
    'create_time',
    'ordersNo',
    'goodsName',
]

# 定义需要模糊查询的字段
FUZZY_FIELDS = [
    'ordersNo',
    'goodsName',
]
# 定义外键字段
FOREIGN_KEYS = [
    'oid',
    'gid',
]

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10       # 每页最多显示的条数
    page_query_param = 'currentPage'   # 查询参数
    page_size_query_param = 'pagesize'
    max_page_size = 100   # 最大页数

#后台分页查询
class selectPageView(generics.GenericAPIView):
    queryset = OrderItem.objects.order_by('-create_time')
    serializer_class = OrderItemSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = OrderItemSerializer
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
                item_serializer = OrderItemSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = OrderItemSerializer(instance=item_queryset, many=True)
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
    queryset = OrderItem.objects.order_by('-create_time')
    serializer_class = OrderItemSerializer
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
            serializer = OrderItemSerializer(instance=item_queryset, many=True)
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
            data = OrderItem.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = OrderItemSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#前端分页查询
class frontPageView(generics.GenericAPIView):
    queryset = OrderItem.objects.order_by('-create_time')
    serializer_class = OrderItemSerializer
    pagination_class = MyPageNumberPagination

    serializer_class = OrderItemSerializer
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
                item_serializer = OrderItemSerializer(instance=item_page, many=True)
                return ResponseHandler.success_with_page(
                    list_data=item_serializer.data,
                    total=total,
                    msg='获取成功'
                )
            serializer = OrderItemSerializer(instance=item_queryset, many=True)
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
    queryset = OrderItem.objects.order_by('-create_time')
    serializer_class = OrderItemSerializer
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
            serializer = OrderItemSerializer(instance=item_queryset, many=True)
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
            data = OrderItem.objects.filter(id=id).first()
            if not data:
                return ResponseHandler.error(msg='数据不存在')
            data_serializer = OrderItemSerializer(instance=data)
            return ResponseHandler.success(data=data_serializer.data, msg='查询成功')
        except Exception as e:
            print("查询出现异常: %s" % e)
            return ResponseHandler.error(msg='查询失败')

#新增
class addView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            
            # 获取购物车ID列表
            cart_ids = dic.get('gids', '').split(',')
            if not cart_ids:
                return ResponseHandler.error(msg='购物车ID不能为空')

            # 生成订单编号
            from datetime import datetime
            no = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # 获取购物车列表和计算总价总量
            from decimal import Decimal
            from myapps.Cart.models import Cart
            from myapps.Goods.models import Goods
            
            total = Decimal('0.00')
            total_num = 0
            cart_list = []
            
            # 查询购物车信息并计算总价
            for cart_id in cart_ids:
                cart = Cart.objects.filter(id=int(cart_id)).first()
                if not cart:
                    continue
                    
                goods = Goods.objects.filter(id=cart.gid_id).first()
                if not goods:
                    continue
                    
                total_num += cart.num
                item_total = Decimal(str(goods.money)) * Decimal(str(cart.num))
                total += item_total.quantize(Decimal('0.00'))
                
                cart_list.append({
                    'cart': cart,
                    'goods': goods,
                    'item_total': item_total
                })

            if not cart_list:
                return ResponseHandler.error(msg='未找到有效的购物车商品')

            # 创建订单
            from myapps.Orders.models import Orders
            order = Orders.objects.create(
                no=no,
                num=total_num,
                total=str(total),
                uid_id=dic.get('uid'),
                remark=dic.get('remark'),
                status='01'
            )

            # 创建订单项并更新商品库存
            for item in cart_list:
                cart = item['cart']
                goods = item['goods']
                item_total = item['item_total']
                
                # 创建订单项
                OrderItem.objects.create(
                    gid_id=cart.gid_id,
                    money=str(item_total),
                    num=cart.num,
                    oid_id=order.id
                )
                
                # 更新商品库存
                goods.num = goods.num - cart.num
                goods.save()
                
                # 删除购物车项
                cart.delete()

            return ResponseHandler.success(msg='下单成功')
            
        except Exception as e:
            print("下单出现异常: %s" % e)
            return ResponseHandler.error(msg='下单失败')

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
            obj = OrderItem.objects.filter(id=id_value).first()
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
            return ResponseHandler.success(data=OrderItemSerializer(obj).data, msg='更新成功')
        except Exception as e:
            print("更新时出现异常: %s" % e)
            return ResponseHandler.error(msg='更新失败')

#删除
class DelView(View):
    def get(self, request):
        try:
            id = request.GET.get("id")
            orderItem = OrderItem.objects.filter(id=id).first()
            if not orderItem:
                return ResponseHandler.error(msg='数据不存在')
            orderItem.delete()
            return ResponseHandler.success(msg='删除成功')
        except Exception as e:
            print("删除时出现异常: %s" % e)
            return ResponseHandler.error(msg='删除失败')

#新增下单视图
class xiadanView(View):
    def post(self, request):
        try:
            dic = json.loads(request.body.decode("utf-8"))
            
            # 生成订单编号
            from datetime import datetime
            no = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # 计算总价
            from decimal import Decimal
            from myapps.Goods.models import Goods
            
            goods = Goods.objects.filter(id=dic.get('gid')).first()
            if not goods:
                return ResponseHandler.error(msg='商品不存在')
                
            total = Decimal('0.00')
            money = Decimal(str(goods.money))
            nums = Decimal(str(dic.get('num')))
            total = (total + money * nums).quantize(Decimal('0.00'))
            
            # 创建订单
            from myapps.Orders.models import Orders
            order = Orders.objects.create(
                no=no,
                num=dic.get('num'),
                total=str(total),
                uid_id=dic.get('uid'),
                remark=dic.get('remark'),
                status='01'
            )
            
            # 创建订单项
            OrderItem.objects.create(
                gid_id=dic.get('gid'),
                money=str(total),
                num=dic.get('num'),
                oid_id=order.id
            )
            
            # 更新商品库存
            goods.num = goods.num - dic.get('num')
            goods.save()
            
            return ResponseHandler.success(msg='下单成功')
            
        except Exception as e:
            print("下单出现异常: %s" % e)
            return ResponseHandler.error(msg='下单失败')

