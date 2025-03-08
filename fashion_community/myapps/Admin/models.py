from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=200, null=True, verbose_name="头像")
    username = models.CharField(max_length=200, null=True, verbose_name="用户名")
    password = models.CharField(max_length=200, null=True, verbose_name="密码")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    class Meta:
        db_table = "admin"

class AdminSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    class Meta:
        model = Admin
        fields = [
            'id',
            'image',
            'username',
            'password',
            'createTime',
        ]
