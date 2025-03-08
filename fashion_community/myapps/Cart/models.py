from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Goods.models import Goods
from myapps.User.models import User

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    gid = models.ForeignKey(Goods, on_delete=models.CASCADE, db_constraint=False)
    num = models.IntegerField(null=True, verbose_name="数量")
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    class Meta:
        db_table = "cart"

class CartSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    gid = serializers.SerializerMethodField()

    def get_gid(self, obj):
        return obj.gid_id if hasattr(obj, 'gid_id') else None

    uid = serializers.SerializerMethodField()

    def get_uid(self, obj):
        return obj.uid_id if hasattr(obj, 'uid_id') else None

    goodsName = serializers.SerializerMethodField()

    def get_goodsName(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.name
        except (Goods.DoesNotExist, AttributeError):
            return None
        return None

    realname = serializers.SerializerMethodField()

    def get_realname(self, obj):
        try:
            if hasattr(obj, 'uid') and obj.uid is not None:
                return obj.uid.realname
        except (User.DoesNotExist, AttributeError):
            return None
        return None
    
    goodsMoney = serializers.SerializerMethodField()

    def get_goodsMoney(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.money
        except (User.DoesNotExist, AttributeError):
            return None
        return None
    
    goodsImage = serializers.SerializerMethodField()

    def get_goodsImage(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.image
        except (User.DoesNotExist, AttributeError):
            return None
        return None
    
    goodsNum = serializers.SerializerMethodField()

    def get_goodsNum(self, obj):
        try:
            if hasattr(obj, 'gid') and obj.gid is not None:
                return obj.gid.num
        except (User.DoesNotExist, AttributeError):
            return None
        return None


    class Meta:
        model = Cart
        fields = [
            'id',
            'gid',
            'num',
            'uid',
            'createTime',
            'goodsName',
            'realname',
            'goodsMoney',
            'goodsImage',
            'goodsNum',
        ]
