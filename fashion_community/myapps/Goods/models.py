from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer
from myapps.Category.models import Category

class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Category, on_delete=models.CASCADE, db_constraint=False)
    image = models.CharField(max_length=200, null=True, verbose_name="商品图片")
    name = models.CharField(max_length=200, null=True, verbose_name="名称")
    remark = models.CharField(max_length=200, null=True, verbose_name="简介")
    money = models.CharField(max_length=200, null=True, verbose_name="价格")
    num = models.IntegerField(null=True, verbose_name="库存")
    content = models.CharField(max_length=200, null=True, verbose_name="商品介绍")
    status = models.CharField(max_length=200, null=True, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="发布时间")
    class Meta:
        db_table = "goods"

class GoodsSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    cid = serializers.SerializerMethodField()

    def get_cid(self, obj):
        return obj.cid_id if hasattr(obj, 'cid_id') else None

    categoryName = serializers.SerializerMethodField()

    def get_categoryName(self, obj):
        try:
            if hasattr(obj, 'cid') and obj.cid is not None:
                return obj.cid.name
        except (Category.DoesNotExist, AttributeError):
            return None
        return None


    class Meta:
        model = Goods
        fields = [
            'id',
            'cid',
            'image',
            'name',
            'remark',
            'money',
            'num',
            'content',
            'status',
            'createTime',
            'categoryName',
        ]
