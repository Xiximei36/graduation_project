from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Orders.models import Orders
from myapps.Goods.models import Goods

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    oid = models.ForeignKey(Orders, on_delete=models.CASCADE, db_constraint=False)
    gid = models.ForeignKey(Goods, on_delete=models.CASCADE, db_constraint=False)
    num = models.IntegerField(null=True, verbose_name="数量")
    money = models.CharField(max_length=200, null=True, verbose_name="金额")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    class Meta:
        db_table = "order_item"

class OrderItemSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    oid = serializers.SerializerMethodField()

    def get_oid(self, obj):
        return obj.oid_id if hasattr(obj, 'oid_id') else None

    gid = serializers.SerializerMethodField()

    def get_gid(self, obj):
        return obj.gid_id if hasattr(obj, 'gid_id') else None

    ordersNo = serializers.SerializerMethodField()

    def get_ordersNo(self, obj):
        try:
            if hasattr(obj, 'oid') and obj.oid is not None:
                return obj.oid.no
        except (Orders.DoesNotExist, AttributeError):
            return None
        return None

    goodsName = serializers.SerializerMethodField()

    def get_goodsName(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.name
        except (Goods.DoesNotExist, AttributeError):
            return None
        return None
    

    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        try:
            if hasattr(obj, 'oid') and obj.oid is not None:
                return obj.oid.status
        except (Goods.DoesNotExist, AttributeError):
            return None
        return None

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'oid',
            'gid',
            'num',
            'money',
            'createTime',
            'ordersNo',
            'goodsName',
            'status',
        ]
