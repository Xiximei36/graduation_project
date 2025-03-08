from django.db import models
from rest_framework import serializers
from myapps.utils.serializers import BaseSerializer

class User(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.CharField(max_length=200, null=True, verbose_name="头像")
    phone = models.CharField(max_length=200, null=True, verbose_name="手机号")
    password = models.CharField(max_length=200, null=True, verbose_name="密码")
    realname = models.CharField(max_length=200, null=True, verbose_name="姓名")
    sex = models.CharField(max_length=200, null=True, verbose_name="性别")
    age = models.CharField(max_length=200, null=True, verbose_name="年龄")
    address = models.CharField(max_length=200, null=True, verbose_name="地址")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="注册时间")
    class Meta:
        db_table = "user"

class UserSerializer(BaseSerializer):
    createTime = serializers.SerializerMethodField()
    def get_createTime(self, obj):
        return self.format_datetime(obj.create_time)

    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'phone',
            'password',
            'realname',
            'sex',
            'age',
            'address',
            'createTime',
        ]
