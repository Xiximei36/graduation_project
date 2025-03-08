from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.User.models import User

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    no = models.CharField(max_length=200, null=True, verbose_name="订单编号")
    num = models.IntegerField(null=True, verbose_name="商品数量")
    total = models.CharField(max_length=200, null=True, verbose_name="总价")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    remark = models.CharField(max_length=200, null=True, verbose_name="备注")
    status = models.CharField(max_length=200, null=True, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="下单时间")
    class Meta:
        db_table = "orders"

class OrdersSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

    realname = serializers.SerializerMethodField()

    def get_realname(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.realname
        except (User.DoesNotExist, AttributeError):
            return None
        return None

    phone = serializers.SerializerMethodField()

    def get_phone(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.phone
        except (User.DoesNotExist, AttributeError):
            return None
        return None

    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.address
        except (User.DoesNotExist, AttributeError):
            return None
        return None

    class Meta:
        model = Orders
        fields = [
            'id',
            'no',
            'num',
            'total',
            'uid',
            'remark',
            'status',
            'createTime',
            'realname',
            'phone',
            'address',
        ]
