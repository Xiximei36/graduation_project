from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, verbose_name="分类名称")
    remark = models.CharField(max_length=200, null=True, verbose_name="描述")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="发布时间")
    class Meta:
        db_table = "category"

class CategorySerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'remark',
            'createTime',
        ]
